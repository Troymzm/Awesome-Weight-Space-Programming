"""Render the bilingual paper tables and BibTeX from the canonical catalog."""

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit


CATALOG = Path("data/catalog.json")
READMES = {
    "en": ("README.md", "| Work | Publication or project status | Type | Relevance |"),
    "zh": ("README.zh-CN.md", "| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |"),
}
TABLE_SEPARATOR = "| --- | --- | --- | --- |"
ARXIV_URL = re.compile(r"https://arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?(?![\w./-])")
ARXIV_ID = re.compile(r"\d{4}\.\d{4,5}")


def normalize_title(title: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", title).casefold() if char.isalnum()
    )


def read_catalog(root: Path) -> dict:
    return json.loads((root / CATALOG).read_text(encoding="utf-8"))


def write_catalog(root: Path, catalog: dict) -> None:
    validate(catalog)
    path = root / CATALOG
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _table_blocks(lines: list[str], language: str) -> dict[str, tuple[int, int]]:
    """Identify the table bodies by heading, leaving all README prose intact."""
    header = READMES[language][1]
    heading = ""
    tables = {}
    for index, line in enumerate(lines):
        match = re.fullmatch(r"#{2,6} (.+)", line.rstrip("\n"))
        if match:
            heading = match[1]
        if line.rstrip("\n") != header:
            continue
        if not heading or heading in tables or index + 1 >= len(lines):
            raise ValueError(f"invalid catalog table at line {index + 1} in {READMES[language][0]}")
        if lines[index + 1].rstrip("\n") != TABLE_SEPARATOR:
            raise ValueError(f"invalid catalog separator under {heading}")
        start = end = index + 2
        while end < len(lines) and lines[end].startswith("| "):
            end += 1
        tables[heading] = start, end
    return tables


def _arxiv_links(row: dict, language: str, arxiv_id: str) -> set[str]:
    text = f"{row['url']} {row[language]['note']}"
    return {match[0] for match in ARXIV_URL.finditer(text) if match[1] == arxiv_id}


def _single_line(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip() or value.splitlines() != [value]:
        raise ValueError(f"expected a nonempty single line for {name}")


def _bib_field_match(entry: str, name: str):
    return re.search(
        rf"^[ \t]*{re.escape(name)}[ \t]*=[ \t]*"
        r'(?P<value>\{(?P<braced>[^\r\n]*)\}|"(?P<quoted>[^\r\n]*)")[ \t]*,?[ \t]*$',
        entry, re.IGNORECASE | re.MULTILINE,
    )


def bib_field(entry: str, name: str) -> str | None:
    match = _bib_field_match(entry, name)
    if match is None:
        return None
    value = match["braced"] if match["braced"] is not None else match["quoted"]
    return value.strip()


def set_bib_field(entry: str, name: str, value: str) -> str:
    match = _bib_field_match(entry, name)
    if match is not None:
        start, end = match.span("value")
        return entry[:start] + "{" + value + "}" + entry[end:]
    body, separator, _ = entry.rpartition("\n}")
    if not separator:
        raise ValueError("cannot append a BibTeX field to a malformed entry")
    body = body.rstrip()
    comma = "" if body.endswith(",") else ","
    return f"{body}{comma}\n  {name} = {{{value}}}\n}}"


def validate(catalog: dict) -> None:
    title_keys = set()
    row_urls = set()
    arxiv_citations = {}
    section_ids = set()
    headings = {language: set() for language in READMES}
    excluded = catalog.get("excluded_arxiv_ids", {})
    if not isinstance(excluded, dict):
        raise ValueError("excluded_arxiv_ids must map arXiv IDs to review reasons")
    for arxiv_id, reason in excluded.items():
        if not ARXIV_ID.fullmatch(arxiv_id):
            raise ValueError(f"invalid excluded arXiv ID: {arxiv_id}")
        _single_line(reason, f"exclusion reason for arXiv:{arxiv_id}")

    for section in catalog["sections"]:
        section_id = section["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", section_id) or section_id in section_ids:
            raise ValueError(f"invalid or duplicate catalog section ID: {section_id}")
        section_ids.add(section_id)
        for language in READMES:
            heading = section["headings"][language]
            _single_line(heading, "section heading")
            if heading in headings[language]:
                raise ValueError(f"duplicate {language} section heading: {heading}")
            headings[language].add(heading)

        for row in section["rows"]:
            title, url = row["title"], row["url"]
            _single_line(title, "title")
            _single_line(url, "URL")
            normalized_title = normalize_title(title)
            normalized_url = url.rstrip("/")
            parsed_url = urlsplit(url)
            if not normalized_title or normalized_title in title_keys:
                raise ValueError(f"invalid or duplicate title: {title}")
            if parsed_url.scheme != "https" or not parsed_url.hostname or re.search(r"\s", url):
                raise ValueError(f"invalid HTTPS URL for {title}")
            if normalized_url in row_urls:
                raise ValueError(f"duplicate catalog URL: {url}")
            title_keys.add(normalized_title)
            row_urls.add(normalized_url)

            for language in READMES:
                for field in ("status", "type", "note"):
                    _single_line(row[language][field], f"{language} {field} for {title}")

            arxiv_id = row.get("arxiv_id")
            primary = ARXIV_URL.fullmatch(url)
            if primary and arxiv_id != primary[1]:
                raise ValueError(f"incorrect arXiv ID for {title}")
            if arxiv_id is not None:
                if arxiv_id in excluded:
                    raise ValueError(f"excluded arXiv ID is still in the catalog: {arxiv_id}")
                if arxiv_id in arxiv_citations:
                    raise ValueError(f"duplicate arXiv ID: {arxiv_id}")
                localized = [
                    _arxiv_links(row, language, arxiv_id)
                    for language in READMES
                ]
                shared = set.intersection(*localized)
                if not shared:
                    raise ValueError(f"missing shared arXiv link for {title}")
                arxiv_citations[arxiv_id] = shared

    citation_keys = set()
    cited_ids = set()
    for entry in catalog["bibliography"]["entries"]:
        key = re.match(r"@[a-zA-Z]+\{([^,\s]+),", entry)
        if not key or key[1] in citation_keys or not entry.endswith("\n}"):
            first_line = entry.partition("\n")[0]
            raise ValueError(f"invalid or duplicate BibTeX entry: {first_line}")
        citation_keys.add(key[1])
        arxiv_id = bib_field(entry, "eprint")
        if arxiv_id is None:
            continue
        citation_url = bib_field(entry, "url")
        if citation_url not in arxiv_citations.get(arxiv_id, ()):
            raise ValueError(f"BibTeX URL does not match the catalog for arXiv:{arxiv_id}")
        if arxiv_id in cited_ids:
            raise ValueError(f"duplicate bibliography entry for arXiv:{arxiv_id}")
        cited_ids.add(arxiv_id)
    missing = arxiv_citations.keys() - cited_ids
    if missing:
        raise ValueError(f"missing BibTeX entries: {', '.join(sorted(missing))}")


def _cell(text: str) -> str:
    return re.sub(r"(?<!\\)\|", r"\\|", text)


def _render_row(row: dict, language: str) -> str:
    title = re.sub(r"([\\\[\]`*_|])", r"\\\1", row["title"])
    title = title.replace("<", "&lt;").replace(">", "&gt;")
    localized = row[language]
    cells = [f"[{title}]({row['url']})", localized["status"], localized["type"], localized["note"]]
    return "| " + " | ".join(map(_cell, cells)) + " |\n"


def render(root: Path, catalog: dict, check: bool = False) -> None:
    validate(catalog)
    outputs = {}
    for language, (name, _) in READMES.items():
        path = root / name
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        tables = _table_blocks(lines, language)
        sections = {section["headings"][language]: section["rows"] for section in catalog["sections"]}
        if tables.keys() != sections.keys():
            raise ValueError(f"catalog headings differ from {name}: {tables.keys() ^ sections.keys()}")
        for heading, (start, end) in reversed(list(tables.items())):
            lines[start:end] = [_render_row(row, language) for row in sections[heading]]
        outputs[path] = "".join(lines)

    bibliography = catalog["bibliography"]
    outputs[root / "references.bib"] = "\n\n".join([bibliography["preamble"], *bibliography["entries"]]) + "\n"
    stale = [path for path, text in outputs.items() if path.read_text(encoding="utf-8") != text]
    if check and stale:
        raise ValueError(f"stale catalog outputs: {', '.join(path.name for path in stale)}")
    for path in stale:
        path.write_text(outputs[path], encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the generated catalog output files")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        render(root, read_catalog(root), check=not args.write)
    except ValueError as error:
        parser.exit(1, f"{error}\n")
