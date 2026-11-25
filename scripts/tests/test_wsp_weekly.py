import shutil
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from wsp_arxiv import ArxivError, ArxivPaper
from wsp_catalog import bib_field, read_catalog, render, write_catalog
from wsp_weekly import bib_entry, new_row, run_weekly


TODAY = date(2026, 11, 30)
NEW_ID = "2611.39201"
BENCH_ID = "2611.18553"
ARTIFACTS = ("data/catalog.json", "README.md", "README.zh-CN.md", "references.bib")


class FakeArxiv:
    def __init__(self, new=(), known=(), error=None, status=None):
        self.new, self.known, self.error = new, known, error
        self.status = status or {}
        self.status_checks = []
        self.query_window = None
        self.tracked = None

    def search(self, start, end):
        self.query_window = start, end
        if self.error:
            raise ArxivError(self.error)
        return self.new

    def lookup(self, ids):
        self.tracked = ids
        return self.known

    def check_status(self, paper):
        self.status_checks.append((paper.arxiv_id, paper.version))
        key = paper.arxiv_id, paper.version
        if key not in self.status:
            raise ArxivError("official version page unavailable")
        return replace(paper, withdrawn=self.status[key])


def record(arxiv_id, title, version=1, author="A. Researcher",
           abstract="An LLM edits neural network weights without gradient training.",
           withdrawn=False, **metadata):
    return ArxivPaper(
        arxiv_id=arxiv_id, version=version, title=title, authors=(author,),
        first_submitted=date(2026, 11, 24), updated=TODAY, categories=("cs.LG",),
        abstract=abstract, withdrawn=withdrawn,
        **metadata,
    )


class WeeklyUpdateTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for path in ARTIFACTS:
            output = self.root / path
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SCRIPTS.parent / path, output)
        # Keep the real section layout while isolating version and cursor fixtures
        # from future catalog changes, including pending weekly proposals.
        catalog = read_catalog(self.root)
        catalog.pop("last_weekly_scan", None)
        existing = record(BENCH_ID, "Fixture WSP Benchmark")
        for section in catalog["sections"]:
            section["rows"] = []
            if section["id"] == "benchmarks":
                section["rows"].append(new_row(existing, ("benchmarks", "A benchmark.", "一个基准。")))
        catalog["bibliography"]["entries"] = [bib_entry(existing)]
        write_catalog(self.root, catalog)
        render(self.root, catalog)
        self.report = self.root / "report.md"

    def proposal(self, client, day=TODAY):
        return run_weekly(self.root, client, day, self.report)

    def snapshot(self):
        return [self.root.joinpath(path).read_bytes() for path in ARTIFACTS]

    def save(self, catalog):
        write_catalog(self.root, catalog)
        render(self.root, catalog)

    def test_bilingual_addition_revision_and_rerun(self):
        new_title = "Tool-Free Weight-Space Programming for Classifier Repair"
        new = record(NEW_ID, new_title)
        revised = record(BENCH_ID, "WeightBench: Revised Evaluation", version=2, author="A. Updated")
        duplicate = record("2611.39200", new_title.lower())
        client = FakeArxiv(new=(new, duplicate), known=(revised,))

        self.assertFalse(self.proposal(client))
        self.assertEqual(client.query_window, (date(2026, 11, 17), TODAY))
        self.assertIn(BENCH_ID, client.tracked)
        body = self.report.read_text(encoding="utf-8")
        self.assertIn("### New records", body)
        self.assertIn("arXiv v1 → v2", body)
        catalog = read_catalog(self.root)
        render(self.root, catalog, check=True)
        self.assertEqual(catalog["last_weekly_scan"], TODAY.isoformat())
        for name in ("README.md", "README.zh-CN.md"):
            content = (self.root / name).read_text(encoding="utf-8")
            self.assertIn(f"[{new_title}](https://arxiv.org/abs/{NEW_ID}v1)", content)
            self.assertIn(f"[{revised.title}](https://arxiv.org/abs/{BENCH_ID}v2)", content)
            self.assertNotIn("2611.39200", content)
        bib = (self.root / "references.bib").read_text(encoding="utf-8")
        self.assertIn(f"eprint = {{{NEW_ID}}}", bib)
        self.assertIn("author = {A. Updated}", bib)

        snapshot = self.snapshot()
        self.assertFalse(self.proposal(client, date(2026, 12, 7)))
        self.assertEqual(self.snapshot(), snapshot)
        self.assertIn("No catalog changes proposed.", self.report.read_text(encoding="utf-8"))

    def test_partial_failure_records_withdrawal_without_advancing_checkpoint(self):
        existing = record(BENCH_ID, "Withdrawn", withdrawn=True)
        client = FakeArxiv(known=(existing,), error="endpoint unavailable")
        self.assertFalse(self.proposal(client))
        catalog = read_catalog(self.root)
        self.assertNotIn("last_weekly_scan", catalog)
        self.assertIn("arXiv withdrawn", (self.root / "README.md").read_text(encoding="utf-8"))
        self.assertIn("arXiv 已撤回", (self.root / "README.zh-CN.md").read_text(encoding="utf-8"))
        self.assertIn("Incomplete scan", self.report.read_text(encoding="utf-8"))
        snapshot = self.snapshot()
        self.assertTrue(self.proposal(client))
        self.assertEqual(self.snapshot(), snapshot)

    def test_empty_scan_leaves_coverage_and_catalog_unchanged(self):
        snapshot = self.snapshot()
        client = FakeArxiv()
        self.assertFalse(self.proposal(client))
        self.assertEqual(snapshot, self.snapshot())
        self.assertIn("Search returned 0 records", self.report.read_text(encoding="utf-8"))

    def test_compact_bibtex_fields_survive_revision(self):
        catalog = read_catalog(self.root)
        entry = catalog["bibliography"]["entries"][0]
        catalog["bibliography"]["entries"][0] = entry.replace("eprint = ", "eprint=").replace(
            "note = ", "note="
        )
        self.save(catalog)

        client = FakeArxiv(known=(record(BENCH_ID, "Revised fixture", version=2),))
        self.assertFalse(self.proposal(client))
        entry = read_catalog(self.root)["bibliography"]["entries"][0]
        self.assertIn(f"eprint={{{BENCH_ID}}}", entry)
        self.assertEqual(bib_field(entry, "url"), f"https://arxiv.org/abs/{BENCH_ID}v2")
        self.assertIn("arXiv v2", bib_field(entry, "note"))

    def test_exclusion_survives_rolling_search(self):
        paper = record(NEW_ID, "Tool-Free Weight-Space Programming for Classifier Repair")
        client = FakeArxiv(new=(paper,))
        self.assertFalse(self.proposal(client))
        catalog = read_catalog(self.root)
        for section in catalog["sections"]:
            section["rows"] = [row for row in section["rows"] if row.get("arxiv_id") != NEW_ID]
        catalog["bibliography"]["entries"] = [
            entry for entry in catalog["bibliography"]["entries"] if bib_field(entry, "eprint") != NEW_ID
        ]
        catalog["excluded_arxiv_ids"] = {NEW_ID: "The target experiment is outside this catalog's scope."}
        self.save(catalog)

        snapshot = self.snapshot()
        self.assertFalse(self.proposal(client, date(2026, 12, 7)))
        self.assertEqual(self.snapshot(), snapshot)
        self.assertIn("No catalog changes proposed.", self.report.read_text(encoding="utf-8"))

    def test_known_alias_is_proposed_with_verified_status(self):
        # Real retrieval regression, arXiv:2611.31979.
        title = "Reading, Writing and Repairing Game-Theoretic Policies in Weight Space"
        paper = record(
            "2611.31979", title, withdrawn=None,
            abstract="A language model reads weights, writes strategies and repairs a recurrent policy.",
        )
        client = FakeArxiv(new=(paper,), status={(paper.arxiv_id, 1): False})
        self.assertFalse(self.proposal(client))
        self.assertEqual(client.status_checks, [(paper.arxiv_id, 1)])
        self.assertIn(title, self.report.read_text(encoding="utf-8"))

    def test_withdrawn_and_unknown_new_status_do_not_enter_catalog(self):
        withdrawn = record(NEW_ID, "Tool-Free Weight-Space Programming for Repair", withdrawn=None)
        unknown = record("2611.39202", "Tool-Free Weight-Space Programming for Reading", withdrawn=None)
        client = FakeArxiv(new=(withdrawn, unknown), status={(withdrawn.arxiv_id, 1): True})
        snapshot = self.snapshot()
        self.assertTrue(self.proposal(client))
        self.assertEqual(self.snapshot(), snapshot)
        body = self.report.read_text(encoding="utf-8")
        self.assertIn(f"status for {unknown.arxiv_id}v1", body)
        self.assertIn("The search checkpoint was retained.", body)

    def test_withdrawn_version_can_be_followed_by_an_active_version(self):
        tombstone = record(BENCH_ID, "Withdrawn revision", version=2, withdrawn=None)
        recovered = record(BENCH_ID, "Restored benchmark", version=3, withdrawn=None)
        client = FakeArxiv(known=(tombstone,), status={(BENCH_ID, 2): True, (BENCH_ID, 3): False})
        self.assertFalse(self.proposal(client))
        self.assertIn("arXiv withdrawn", (self.root / "README.md").read_text(encoding="utf-8"))
        client.known = (recovered,)
        self.assertFalse(self.proposal(client, date(2026, 12, 7)))
        self.assertIn("active version after withdrawal", self.report.read_text(encoding="utf-8"))
        for name, removed in (("README.md", "arXiv withdrawn"), ("README.zh-CN.md", "arXiv 已撤回"),
                              ("references.bib", "arXiv withdrawn")):
            text = (self.root / name).read_text(encoding="utf-8")
            self.assertNotIn(removed, text)
            self.assertIn(f"{BENCH_ID}v3", text)

        snapshot = self.snapshot()
        self.assertFalse(self.proposal(client, date(2026, 12, 14)))
        self.assertEqual(self.snapshot(), snapshot)
        self.assertEqual(client.status_checks, [(BENCH_ID, 2), (BENCH_ID, 3)])


if __name__ == "__main__":
    unittest.main()
