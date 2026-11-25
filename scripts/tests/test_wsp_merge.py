import sys
import unittest
from copy import deepcopy
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from wsp_merge import _readme_prose, merge_catalogs


def add_paper(catalog, arxiv_id, title):
    url = f"https://arxiv.org/abs/{arxiv_id}v1"
    catalog["sections"][0]["rows"].append({
        "title": title,
        "url": url,
        "arxiv_id": arxiv_id,
        "en": {"status": "arXiv preprint", "type": "Interpretation", "note": "A test reference."},
        "zh": {"status": "arXiv 预印本", "type": "解释", "note": "一条测试引用。"},
    })
    key = arxiv_id.replace(".", "_")
    catalog["bibliography"]["entries"].append(
        f"@misc{{arxiv_{key},\n  eprint={{{arxiv_id}}},\n  url = {{{url}}}\n}}"
    )


class StructuredMergeTest(unittest.TestCase):
    def setUp(self):
        self.base = {
            "sections": [{"id": "start-here", "headings": {"en": "Start here", "zh": "入门导读"}, "rows": []}],
            "bibliography": {"preamble": "% Bibliography", "entries": []},
        }
        add_paper(self.base, "2611.18553", "A Shared Benchmark")
        self.main = deepcopy(self.base)
        self.pending = deepcopy(self.base)

    def test_independent_papers_and_bibliography_tail_appends_merge(self):
        add_paper(self.main, "2611.39281", "A Human-Curated Paper")
        add_paper(self.pending, "2611.39282", "A Pending Automated Paper")
        self.main["last_weekly_scan"] = "2026-11-29"
        self.pending["last_weekly_scan"] = "2026-12-01"

        merged = merge_catalogs(self.base, self.main, self.pending)

        self.assertEqual(merged["last_weekly_scan"], "2026-12-01")
        self.assertEqual(
            [row["arxiv_id"] for row in merged["sections"][0]["rows"][-2:]],
            ["2611.39281", "2611.39282"],
        )
        self.assertEqual(
            merged["bibliography"]["entries"][-2:],
            [self.main["bibliography"]["entries"][-1], self.pending["bibliography"]["entries"][-1]],
        )

    def test_conflicting_edits_to_one_paper_report_its_id(self):
        for catalog, note in ((self.main, "Human reading."), (self.pending, "Pending reading.")):
            paper = next(row for section in catalog["sections"] for row in section["rows"]
                         if row.get("arxiv_id") == "2611.18553")
            paper["en"]["note"] = note

        with self.assertRaisesRegex(ValueError, r"Conflicting paper edits for arXiv:2611\.18553"):
            merge_catalogs(self.base, self.main, self.pending)

    def test_human_note_and_version_status_cache_coexist_on_one_row(self):
        self.main["sections"][0]["rows"][0]["en"]["note"] = "Curator checked the controls."
        self.pending["sections"][0]["rows"][0]["arxiv_status_version"] = 1

        paper = merge_catalogs(self.base, self.main, self.pending)["sections"][0]["rows"][0]
        self.assertEqual(paper["en"]["note"], "Curator checked the controls.")
        self.assertEqual(paper["arxiv_status_version"], 1)

    def test_current_exclusions_remove_pending_paper_and_citation(self):
        self.main["excluded_arxiv_ids"] = {"2611.39281": "Outside scope"}
        self.pending["excluded_arxiv_ids"] = {"2611.39283": "Duplicate"}
        add_paper(self.pending, "2611.39281", "An Excluded Paper")
        add_paper(self.pending, "2611.39282", "A Pending Automated Paper")

        merged = merge_catalogs(self.base, self.main, self.pending)

        self.assertEqual(merged["excluded_arxiv_ids"], {
            "2611.39281": "Outside scope", "2611.39283": "Duplicate",
        })
        self.assertEqual(merged["sections"][0]["rows"][-1]["arxiv_id"], "2611.39282")
        self.assertNotIn("2611.39281", "\n".join(merged["bibliography"]["entries"]))

    def test_table_rows_do_not_count_as_prose_changes(self):
        table_row = "| [Benchmark](https://arxiv.org/abs/2611.18553) | preprint | Benchmark | Test |"
        content = (
            "## Start here\n\n| Work | Publication or project status | Type | Relevance |\n"
            "| --- | --- | --- | --- |\n" + table_row + "\n\n## Notes\n"
        )
        original = _readme_prose(content, "en")
        self.assertEqual(original, _readme_prose(content.replace(table_row, table_row + "\n" + table_row), "en"))
        self.assertNotEqual(original, _readme_prose(content + "\nHuman prose.\n", "en"))


if __name__ == "__main__":
    unittest.main()
