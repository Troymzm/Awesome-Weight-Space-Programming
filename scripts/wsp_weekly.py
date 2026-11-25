"""Propose a weekly arXiv update to the bilingual WSP catalog."""

import argparse
import re
import unicodedata
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote

from wsp_arxiv import ArxivClient, ArxivError
from wsp_catalog import normalize_title, read_catalog, render, write_catalog

BASELINE = date(2026, 11, 25)
ARXIV_URL = "https://arxiv.org/abs/"
BIB_ID = re.compile(r"^\s*eprint = \{([^}]+)\}", re.M)
DOI_URL = re.compile(r"https://(?:dx\.)?doi\.org/(10\.[^\s)]+)", re.I)
WSP = re.compile(r"\b(?:weight[\s-]+space[\s-]+programming|self[\s-]+wsp)\b")
WEIGHTS = re.compile(r"\b(?:weights?|parameters?|tensors?|checkpoints?)\b")
EDIT = re.compile(r"\b(?:edit\w*|rewrit\w*|writ\w*|repair\w*|compil\w*|inspect\w*|read\w*)\b")
AGENT = re.compile(r"\b(?:llms?|language models?|coding agents?|agentic)\b")
LIMIT = re.compile(r"\b(?:gradient.free|(?:no|without) (?:gradients?|training|backpropagation)|tool.free)\b")
TOPICS = (
    (r"\b(?:replicat\w*|reproduc\w*|negative results?)\b", "replications-and-controls",
     "Reports a replication or control study related to weight-space programming.",
     "报告与权重空间编程相关的复现或对照研究。"),
    (r"\b(?:benchmark\w*|evaluating language models as weight.space programmers)\b", "benchmarks",
     "Proposes or studies evaluation tasks for weight-space programming.",
     "提出或研究用于评估权重空间编程的任务。"),
    (r"\b(?:self[\s-]+wsp|self[\s-]+edit\w*|self[\s-]+rewrit\w*|its own weights)\b",
     "self-editing-and-iterative-feedback",
     "Studies self-editing of model weights.", "研究模型对自身权重的编辑。"),
    (r"\b(?:repair\w*|adapt\w*|fault\w*|edit\w*)\b", "repair-and-adapt",
     "Studies model repair or adaptation through parameter changes.",
     "研究通过参数修改进行模型修复或适配。"),
    (r"\b(?:install\w*|compos\w*|transfer\w*)\b", "install-and-compose",
     "Studies capability installation, transfer or composition in weight space.",
     "研究权重空间中的能力写入、迁移或组合。"),
    (r"\b(?:writ\w*|compil\w*|synthes\w*|construct\w*)\b", "write-and-compile",
     "Studies the construction of executable network weights.", "研究如何构造可执行的网络权重。"),
    (r"\b(?:read\w*|diagnos\w*|inspect\w*|audit\w*)\b", "read-and-diagnose",
     "Studies information that can be recovered from model weights.", "研究可从模型权重中恢复的信息。"),
)


def search_text(value):
    return unicodedata.normalize("NFKC", value).casefold().translate(
        str.maketrans({dash: "-" for dash in "‐‑‒–—−"})
    )


def paper_url(paper):
    return f"{ARXIV_URL}{paper.arxiv_id}v{paper.version}"


def latex(value):
    escapes = {
        "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "&": r"\&",
        "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(escapes.get(char, char) for char in value)


def bib_authors(paper):
    return " and ".join(latex(author).replace(" and ", " {and} ") for author in paper.authors)


def bib_entry(paper):
    key = re.sub(r"[^a-zA-Z0-9]+", "_", paper.arxiv_id)
    return "\n".join((
        f"@misc{{arxiv_{key},",
        f"  title = {{{{{latex(paper.title)}}}}},",
        f"  author = {{{bib_authors(paper)}}},",
        f"  year = {{{paper.first_submitted.year}}},",
        "  archivePrefix = {arXiv},",
        f"  eprint = {{{paper.arxiv_id}}},",
        f"  url = {{{paper_url(paper)}}},",
        f"  note = {{arXiv preprint, v{paper.version}}}",
        "}",
    ))


def arxiv_link(arxiv_id):
    return re.compile(r"https?://(?:www\.)?arxiv\.org/abs/" + re.escape(arxiv_id)
                      + r"(?:v\d+)?(?![\d.v])")


def version_in_row(row):
    version = row.get("arxiv_version", 1)
    for text in (row["url"], row["en"]["note"], row["zh"]["note"]):
        for url in arxiv_link(row["arxiv_id"]).findall(text):
            if (match := re.search(r"v(\d+)$", url)):
                version = max(version, int(match[1]))
    return version


def topic_for(title, abstract):
    for text in (title, abstract):
        for pattern, section, en, zh in TOPICS:
            if re.search(pattern, text):
                return section, en, zh
    return ("replications-and-controls", "Examines weight-space programming on neural models.",
            "研究神经模型上的权重空间编程。")


def screen(title, abstract):
    text = f"{title} {abstract}"
    direct = WEIGHTS.search(text) and EDIT.search(text) and AGENT.search(text)
    if WSP.search(title) and WEIGHTS.search(text):
        return "explicit WSP title"
    if WSP.search(abstract) and direct:
        return "WSP in abstract with direct weight operations"
    if direct and LIMIT.search(text) and (
        ("weight" in title and EDIT.search(title)) or ("agentic coding" in title and LIMIT.search(title))
    ):
        return "agentic weight operations with a restricted optimization regime"
    return None


def new_row(paper, topic):
    section, en, zh = topic
    en_type, zh_type = ("Benchmark", "基准") if section == "benchmarks" else ("Empirical study", "实证研究")
    return {
        "title": paper.title, "url": paper_url(paper), "arxiv_id": paper.arxiv_id,
        "arxiv_version": paper.version,
        "en": {"status": f"arXiv preprint · {paper.first_submitted} · v{paper.version}",
               "type": en_type, "note": en},
        "zh": {"status": f"arXiv 预印本 · {paper.first_submitted} · v{paper.version}",
               "type": zh_type, "note": zh},
    }


def append_status(status, label, version, newer, withdrawn):
    if newer:
        if status.startswith(("arXiv preprint · ", "arXiv 预印本 · ")):
            status = re.sub(r" · v\d+(?= · |$)", "", status) + f" · v{version}"
        elif re.search(r" · arXiv v\d+(?= · |$)", status):
            status = re.sub(r" · arXiv v\d+(?= · |$)", f" · arXiv v{version}", status)
        else:
            status += f" · arXiv v{version}"
    if withdrawn and label not in status:
        status += f" · {label}"
    return status


def refresh_row(row, paper, bib, bib_index):
    old_version = version_in_row(row)
    newer = paper.version > old_version
    withdrawn = paper.withdrawn and not row.get("arxiv_withdrawn")
    preprint = row["en"]["status"].startswith("arXiv preprint")
    source = arxiv_link(paper.arxiv_id)
    changes = []
    if newer:
        changes.append(f"arXiv v{old_version} → v{paper.version}")
        row["arxiv_version"] = paper.version
        if preprint and source.fullmatch(row["url"]) and not paper.withdrawn:
            if row["title"] != paper.title:
                changes.append("arXiv title changed")
            row["title"] = paper.title
        row["url"] = source.sub(paper_url(paper), row["url"])
        for language in ("en", "zh"):
            row[language]["note"] = source.sub(paper_url(paper), row[language]["note"])
    if withdrawn:
        row["arxiv_withdrawn"] = True
        changes.append("arXiv marked withdrawn")
    journal = paper.journal_ref.strip()
    if preprint and journal and journal != row.get("arxiv_journal_ref"):
        row["arxiv_journal_ref"] = journal
        changes.append(f"verify arXiv journal reference: {journal}")
    if not (newer or withdrawn):
        return changes

    for language, label in (("en", "arXiv withdrawn"), ("zh", "arXiv 已撤回")):
        row[language]["status"] = append_status(
            row[language]["status"], label, paper.version, newer, withdrawn
        )
    index = bib_index[paper.arxiv_id]
    entry = bib[index]
    if newer:
        entry = source.sub(paper_url(paper), entry)
        if preprint and not paper.withdrawn:
            entry = re.sub(r"^  title = .*,$", lambda _: f"  title = {{{{{latex(row['title'])}}}}},",
                           entry, count=1, flags=re.M)
            entry = re.sub(r"^  author = .*,$", lambda _: f"  author = {{{bib_authors(paper)}}},",
                           entry, count=1, flags=re.M)
    annotation = "arXiv withdrawn" if withdrawn else f"arXiv v{paper.version}"
    entry = re.sub(r"^(  note = \{)(.*)(\})$",
                   lambda m: m[1] + re.sub(r", (?:arXiv )?v\d+$", "", m[2]) + ", " + annotation + m[3],
                   entry, count=1, flags=re.M)
    bib[index] = entry
    return changes


def markdown_text(value):
    value = " ".join(value.split())
    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("@", "&#64;")
    return re.sub(r"([\\\[\]()*_\x60|])", r"\\\1", value)


def report_line(paper, note):
    return f"- [{markdown_text(paper.title)}]({paper_url(paper)}) · {markdown_text(note)}"


def run_weekly(root, client, today, report_path):
    catalog = read_catalog(root)
    render(root, catalog, check=True)
    sections = {section["id"]: section["rows"] for section in catalog["sections"]}
    rows = [row for group in sections.values() for row in group]
    tracked = {row["arxiv_id"]: row for row in rows if row.get("arxiv_id")}
    bib = catalog["bibliography"]["entries"]
    bib_index = {match[1]: i for i, entry in enumerate(bib) if (match := BIB_ID.search(entry))}

    previous = date.fromisoformat(catalog.get("last_weekly_scan", BASELINE.isoformat()))
    start = min(today - timedelta(days=13), previous - timedelta(days=3))
    found, refreshed, failures = [], [], []
    try:
        found = client.search(start, today)
    except ArxivError as exc:
        failures.append(f"arXiv new submissions: {exc}")
    try:
        refreshed = client.lookup(sorted(tracked))
    except ArxivError as exc:
        failures.append(f"arXiv existing records: {exc}")

    updated, additions, screened_out = [], [], []
    for paper in sorted(refreshed, key=lambda p: p.arxiv_id):
        changes = refresh_row(tracked[paper.arxiv_id], paper, bib, bib_index)
        if changes:
            updated.append(report_line(paper, "; ".join(changes)))

    titles = {normalize_title(row["title"]) for row in rows}
    dois = {
        unquote(doi).casefold()
        for row in rows
        for doi in (row.get("doi", ""), *DOI_URL.findall(row["url"]), *DOI_URL.findall(row["en"]["note"]))
        if doi
    }
    for paper in sorted(found, key=lambda p: (p.first_submitted, p.arxiv_id), reverse=True):
        key = normalize_title(paper.title)
        doi = paper.doi.casefold()
        if paper.withdrawn or paper.arxiv_id in tracked or key in titles or (doi and doi in dois):
            continue
        title, abstract = map(search_text, (paper.title, paper.abstract))
        reason = screen(title, abstract)
        if not reason:
            if WSP.search(abstract) and len(screened_out) < 20:
                screened_out.append(report_line(paper, "manual screening suggested"))
            continue
        topic = topic_for(title, abstract)
        row = new_row(paper, topic)
        if doi:
            row["doi"] = paper.doi
            dois.add(doi)
        if paper.journal_ref:
            row["arxiv_journal_ref"] = paper.journal_ref
            reason += f"; verify arXiv journal reference: {paper.journal_ref}"
        sections[topic[0]].append(row)
        tracked[paper.arxiv_id] = row
        titles.add(key)
        bib.append(bib_entry(paper))
        additions.append(report_line(paper, reason))

    changed = bool(additions or updated)
    if changed:
        if not failures:
            catalog["last_weekly_scan"] = today.isoformat()
        render(root, catalog)
        write_catalog(root, catalog)
        render(root, read_catalog(root), check=True)

    parts = [
        "## Weekly WSP review",
        f"arXiv submission window (UTC) · {start} through {today}.",
        f"Search returned {len(found)} records. Rechecked {len(refreshed)} catalog IDs.",
        "Review the linked sources before merging. Check the contribution category, "
        "experimental scope, publication status and both language descriptions.",
    ]
    if failures:
        parts.append("Incomplete scan. The search checkpoint was retained.")
    for heading, items in (("New records", additions), ("Changes to existing records", updated),
                           ("Other candidates", screened_out),
                           ("Source failures", [f"- {markdown_text(error)}" for error in failures])):
        if items:
            parts.append(f"### {heading}\n\n" + "\n".join(items))
    if not changed:
        parts.append("No catalog changes proposed.")
    report_path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return bool(failures) and not changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True, help="Write the proposal summary here.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    failed = run_weekly(root, ArxivClient(), datetime.now(timezone.utc).date(), args.report)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
