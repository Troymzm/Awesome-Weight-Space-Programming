"""Reconcile independent catalog edits when the update branch diverges."""

import argparse
import json
import re
import subprocess
from copy import deepcopy
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from wsp_catalog import (
    CATALOG,
    READMES,
    _table_blocks,
    bib_field,
    read_catalog,
    render,
    validate,
    write_catalog,
)


_MISSING = object()
_SPECIAL_FIELDS = {"sections", "bibliography", "excluded_arxiv_ids", "last_weekly_scan"}
_BIB_KEY = re.compile(r"@[a-zA-Z]+\{([^,\s]+),")


def _merge_index(base, main, pending, label, *, merge_fields=False, path=""):
    """Prefer the existing main order and append pending-only keys."""
    result = {}
    for key in dict.fromkeys((*main, *pending, *base)):
        before = base.get(key, _MISSING)
        ours = main.get(key, _MISSING)
        theirs = pending.get(key, _MISSING)
        if ours == theirs or theirs == before:
            chosen = ours
        elif ours == before:
            chosen = theirs
        elif merge_fields and all(isinstance(value, dict) for value in (before, ours, theirs)):
            chosen = _merge_index(
                before, ours, theirs, label, merge_fields=True, path=f"{path}{key}."
            )
        else:
            raise ValueError(f"Conflicting {label} edits for {path}{key}. Resolve them in the review branch.")
        if chosen is not _MISSING:
            result[key] = chosen
    return result


def _section_index(catalog):
    return {
        section["id"]: {key: value for key, value in section.items() if key != "rows"}
        for section in catalog["sections"]
    }


def _row_index(catalog, excluded):
    rows = {}
    for section in catalog["sections"]:
        for row in section["rows"]:
            arxiv_id = row.get("arxiv_id")
            if arxiv_id in excluded:
                continue
            key = f"arXiv:{arxiv_id}" if arxiv_id else row["url"].rstrip("/")
            rows[key] = {"section": section["id"], "row": row}
    return rows


def _bib_index(catalog, excluded):
    entries = {}
    for entry in catalog["bibliography"]["entries"]:
        if bib_field(entry, "eprint") in excluded:
            continue
        entries[_BIB_KEY.match(entry)[1]] = entry
    return entries


def merge_catalogs(base, main, pending):
    """Keep independent edits and report disagreements about the same record."""
    catalogs = (base, main, pending)
    for catalog in catalogs:
        validate(catalog)

    excluded = _merge_index(
        *(catalog.get("excluded_arxiv_ids", {}) for catalog in catalogs), "exclusion"
    )
    sections = {
        key: {**metadata, "rows": []}
        for key, metadata in _merge_index(
            *(_section_index(catalog) for catalog in catalogs), "section"
        ).items()
    }
    rows = _merge_index(
        *(_row_index(catalog, excluded) for catalog in catalogs), "paper", merge_fields=True
    )
    for key, located in rows.items():
        section_id, row = located["section"], located["row"]
        if section_id not in sections:
            raise ValueError(f"Paper {key} refers to a removed section {section_id}.")
        sections[section_id]["rows"].append(row)

    bibliography = _merge_index(
        *({key: value for key, value in catalog["bibliography"].items() if key != "entries"}
          for catalog in catalogs), "bibliography metadata"
    )
    bibliography["entries"] = list(
        _merge_index(*(_bib_index(catalog, excluded) for catalog in catalogs), "citation").values()
    )
    result = _merge_index(
        *({key: value for key, value in catalog.items() if key not in _SPECIAL_FIELDS}
          for catalog in catalogs), "catalog metadata"
    )
    result["sections"] = list(sections.values())
    result["bibliography"] = bibliography
    if excluded or any("excluded_arxiv_ids" in catalog for catalog in catalogs):
        result["excluded_arxiv_ids"] = excluded
    scans = [catalog["last_weekly_scan"] for catalog in (main, pending) if "last_weekly_scan" in catalog]
    if scans:
        result["last_weekly_scan"] = max(scans, key=date.fromisoformat)

    validate(result)
    return deepcopy(result)


def _git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, encoding="utf-8"
    ).stdout


def _readme_prose(text, language):
    lines = text.splitlines(keepends=True)
    for start, end in reversed(list(_table_blocks(lines, language).values())):
        del lines[start:end]
    return "".join(lines)


def reconcile(root, base_ref, pending_ref):
    main, pending = (
        _git(root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").strip()
        for ref in (base_ref, pending_ref)
    )
    ancestor = _git(root, "merge-base", main, pending).strip()
    base_catalog, main_catalog, pending_catalog = (
        json.loads(_git(root, "show", f"{revision}:{CATALOG.as_posix()}"))
        for revision in (ancestor, main, pending)
    )
    if read_catalog(root) != main_catalog:
        raise ValueError("The checked-out catalog differs from the main branch.")
    render(root, main_catalog, check=True)

    # The regenerated table bodies must be determined by catalog.json on both
    # branches. Preserve main prose and require explicit review of pending prose.
    with TemporaryDirectory() as temporary:
        pending_files = Path(temporary)
        for language, (name, _) in READMES.items():
            text = _git(root, "show", f"{pending}:{name}")
            before = _git(root, "show", f"{ancestor}:{name}")
            if _readme_prose(text, language) != _readme_prose(before, language):
                raise ValueError(f"Pending changes outside the catalog tables in {name}. Review them before merging.")
            (pending_files / name).write_text(text, encoding="utf-8")
        (pending_files / "references.bib").write_text(
            _git(root, "show", f"{pending}:references.bib"), encoding="utf-8"
        )
        render(pending_files, pending_catalog, check=True)

    merged = merge_catalogs(base_catalog, main_catalog, pending_catalog)
    render(root, merged)
    write_catalog(root, merged)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_ref", help="reference for the checked-out main catalog")
    parser.add_argument("pending_ref", help="reference for the pending update branch")
    args = parser.parse_args()
    try:
        reconcile(Path(__file__).resolve().parents[1], args.base_ref, args.pending_ref)
    except (ValueError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        parser.exit(1, f"{detail}\n")
