"""Summarize the full catalog proposal in a GitHub pull request."""

import argparse
import json
import subprocess
from pathlib import Path

from wsp_catalog import ARXIV_URL, CATALOG, read_catalog
from wsp_weekly import markdown_text

START = "<!-- wsp-weekly:start -->"
END = "<!-- wsp-weekly:end -->"
INTRO = "Review the source records and bilingual descriptions before merging."
LEGACY_HEADER = INTRO + "\n\n## Latest scan\n"
GROUP_LIMIT = 35


def indexed_rows(catalog):
    return {
        row.get("arxiv_id") or row["url"].rstrip("/"): (section["headings"]["en"], row)
        for section in catalog["sections"]
        for row in section["rows"]
    }


def source_link(title, url):
    url = url.replace("<", "%3C").replace(">", "%3E")
    return f"[{markdown_text(title)}](<{url}>)"


def changes_for_reviewer(entry):
    section, row = entry
    return section, {key: value for key, value in row.items() if key != "arxiv_status_version"}


def describe(entry, previous=None):
    section, row = entry
    text = (f"- {source_link(row['title'], row['url'])} · {markdown_text(section)}"
            f" · {markdown_text(row['en']['status'])}")
    identifier = row.get("arxiv_id")
    if identifier and not ARXIV_URL.fullmatch(row["url"]):
        evidence = next((match[0] for match in ARXIV_URL.finditer(row["en"].get("note", ""))
                         if match[1] == identifier), None)
        if evidence:
            text += f" · {source_link('arXiv record', evidence)}"
    journal = row.get("arxiv_journal_ref")
    if journal and (not previous or journal != previous[1].get("arxiv_journal_ref")):
        text += f" · Verify the arXiv journal reference {markdown_text(journal)}."
    if previous and row["url"] != previous[1]["url"]:
        text += f" · {source_link('Previous source', previous[1]['url'])}"
    return text


def add_group(lines, title, items):
    if not items:
        return
    lines.extend(("", f"### {title} ({len(items)})", ""))
    lines.extend(items[:GROUP_LIMIT])
    if len(items) > GROUP_LIMIT:
        lines.append(f"- See Files changed for {len(items) - GROUP_LIMIT} more.")


def catalog_summary(base, proposed):
    before, after = indexed_rows(base), indexed_rows(proposed)
    lines = [START, "## Pending catalog changes", "",
             "Summary of the catalog diff against the default branch. "
             "Each record links to its primary source."]
    add_group(lines, "New records", [describe(after[key]) for key in after if key not in before])
    add_group(lines, "Updated records",
              [describe(after[key], before[key]) for key in after
               if key in before and changes_for_reviewer(after[key]) != changes_for_reviewer(before[key])])
    add_group(lines, "Removed records", [describe(before[key]) for key in before if key not in after])

    previous_exclusions = base.get("excluded_arxiv_ids", {})
    exclusions = proposed.get("excluded_arxiv_ids", {})
    decisions = []
    for key in sorted(previous_exclusions.keys() | exclusions.keys()):
        if exclusions.get(key) == previous_exclusions.get(key):
            continue
        status = "excluded from automatic proposals" if key in exclusions else "eligible again"
        decisions.append(f"- [{markdown_text(key)}](<https://arxiv.org/abs/{key}>) · {status}")
    add_group(lines, "Review decisions", decisions)

    if proposed["bibliography"] != base["bibliography"]:
        lines.extend(("", "See Files changed for bibliography updates."))
    lines.extend(("", END))
    return "\n".join(lines)


def replace_summary(existing, summary):
    if existing.count(START) == 1 and existing.count(END) == 1:
        start, end = existing.index(START), existing.index(END)
        if start < end:
            return existing[:start] + summary + existing[end + len(END):]
    if START in existing or END in existing:
        raise ValueError("malformed managed summary in the existing pull request body")
    if existing.startswith(LEGACY_HEADER):
        # Keep notes in a legacy body while distinguishing them from the current diff.
        existing = existing.replace("## Latest scan", "## Previous scan", 1)
    return (existing or INTRO).rstrip() + "\n\n" + summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_ref", help="default branch Git reference")
    parser.add_argument("existing", type=Path, help="JSON response from the list-open-PR API")
    parser.add_argument("body", type=Path, help="write the desired body here")
    args = parser.parse_args()
    root = Path.cwd()
    base = json.loads(subprocess.check_output(
        ["git", "show", f"{args.base_ref}:{CATALOG.as_posix()}"],
        cwd=root,
        encoding="utf-8",
    ))
    existing = json.loads(args.existing.read_text(encoding="utf-8"))
    pull_request = existing[0] if existing else None
    current = (pull_request["body"] or "") if pull_request else ""
    body = replace_summary(current, catalog_summary(base, read_catalog(root)))
    args.body.write_text(body, encoding="utf-8", newline="\n")
    number = pull_request["number"] if pull_request else 0
    print(number, int(body != current))


if __name__ == "__main__":
    main()
