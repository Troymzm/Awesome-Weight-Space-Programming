import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from wsp_pr import END, INTRO, START, catalog_summary, replace_summary


def record(identifier, title, version=1, **extra):
    return {
        "arxiv_id": identifier,
        "title": title,
        "url": f"https://arxiv.org/abs/{identifier}v{version}",
        "en": {"status": f"arXiv preprint · v{version}"},
        **extra,
    }


def catalog(rows, exclusions=None, citations=()):
    return {
        "sections": [{"headings": {"en": "Benchmarks"}, "rows": rows}],
        "bibliography": {"entries": list(citations)},
        "excluded_arxiv_ids": exclusions or {},
    }


class PullRequestSummaryTest(unittest.TestCase):
    def test_summary_covers_all_pending_rows_and_exclusions(self):
        old = record("2601.00001", "Previously proposed")
        newer = record("2601.00001", "Revised paper", 2, arxiv_journal_ref="Venue 2026")
        deleted = record("2601.00002", "Removed paper")
        first = record("2601.00003", "First new paper")
        second = record("2601.00004", "Second new paper")
        base = catalog([old, deleted], {"2601.00005": "old exclusion"})
        proposed = catalog([newer, first, second], {"2601.00006": "reviewed"}, ["citation"])

        body = catalog_summary(base, proposed)
        self.assertIn("### New records (2)", body)
        self.assertIn("First new paper", body)
        self.assertIn("Second new paper", body)
        self.assertIn("### Updated records (1)", body)
        self.assertIn("(<https://arxiv.org/abs/2601.00001v2>)", body)
        self.assertIn("Venue 2026", body)
        self.assertIn("[Previous source](<https://arxiv.org/abs/2601.00001v1>)", body)
        self.assertIn("### Removed records (1)", body)
        self.assertIn("### Review decisions (2)", body)
        self.assertIn("bibliography updates", body)

    def test_retry_reconciles_stale_body_and_keeps_review_notes(self):
        previous = f"Notes before\n\n{START}\nOld summary\n{END}\n\nNotes after."
        expected = f"{START}\nCurrent cumulative evidence\n{END}"
        updated = replace_summary(previous, expected)
        self.assertEqual(updated, f"Notes before\n\n{expected}\n\nNotes after.")
        self.assertEqual(replace_summary(updated, expected), updated)

    def test_only_substantive_changes_are_listed(self):
        previous = record("2601.00001", "Verified old paper")
        cached = {**previous, "arxiv_status_version": 1}
        self.assertEqual(catalog_summary(catalog([previous]), catalog([cached])),
                         catalog_summary(catalog([previous]), catalog([previous])))

    def test_arxiv_evidence_accompanies_a_venue_link(self):
        source = record("2601.00001", "Paper from proceedings")
        primary = "https://example.test/proceedings"
        source["en"]["note"] = f"[Preprint]({source['url']})"
        source["url"] = primary
        body = catalog_summary(catalog([]), catalog([source]))
        self.assertIn(f"(<{primary}>)", body)
        self.assertIn("[arXiv record](<https://arxiv.org/abs/2601.00001v1>)", body)

    def test_legacy_scan_is_retained_as_history(self):
        previous = f"{INTRO}\n\n## Latest scan\n\nReview notes."
        next_summary = f"{START}\nCurrent cumulative evidence\n{END}"
        updated = replace_summary(previous, next_summary)
        self.assertIn("## Previous scan\n\nReview notes.", updated)
        self.assertEqual(replace_summary(updated, next_summary), updated)

    def test_damaged_marker_preserves_existing_body(self):
        with self.assertRaisesRegex(ValueError, "malformed managed summary"):
            replace_summary(f"Reviewer notes\n{START}", f"{START}\nNew\n{END}")


if __name__ == "__main__":
    unittest.main()
