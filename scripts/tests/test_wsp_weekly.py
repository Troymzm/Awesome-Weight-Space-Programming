import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from wsp_arxiv import ArxivError, ArxivPaper
from wsp_catalog import read_catalog, render, write_catalog
from wsp_weekly import bib_entry, new_row, run_weekly


TODAY = date(2026, 11, 30)
NEW_ID = "2611.39201"
BENCH_ID = "2611.18553"
ARTIFACTS = ("data/catalog.json", "README.md", "README.zh-CN.md", "references.bib")


class FakeArxiv:
    def __init__(self, new=(), known=(), error=None):
        self.new, self.known, self.error = new, known, error
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


def record(arxiv_id, title, version=1, author="A. Researcher", **metadata):
    return ArxivPaper(
        arxiv_id=arxiv_id, version=version, title=title, authors=(author,),
        first_submitted=date(2026, 11, 24), updated=TODAY, categories=("cs.LG",),
        abstract="An LLM edits neural network weights without gradient training.",
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


if __name__ == "__main__":
    unittest.main()
