from datetime import date
import unittest
from unittest.mock import patch

from scripts.wsp_arxiv import ArxivClient, ArxivError, ArxivPaper, _parse_feed


def feed(entries="", total=0, start=0):
    return f"""<feed xmlns="http://www.w3.org/2005/Atom"
                     xmlns:o="http://a9.com/-/spec/opensearch/1.1/"
                     xmlns:a="http://arxiv.org/schemas/atom">
      <o:totalResults>{total}</o:totalResults>
      <o:startIndex>{start}</o:startIndex>
      {entries}
    </feed>""".encode()


def entry(comment):
    return f"""<entry>
      <id>http://arxiv.org/abs/2611.00001v2</id>
      <title>Weights &amp; Computation</title>
      <author><name>Example Author</name></author>
      <published>2026-11-25T23:50:00-05:00</published>
      <updated>2026-11-28T00:00:00Z</updated>
      <summary>We study an experiment that was withdrawn from another paper.</summary>
      <category term="cs.LG"/>
      <a:comment>{comment}</a:comment>
      <a:doi>10.1234/test</a:doi>
      <a:journal_ref>Example Proceedings</a:journal_ref>
    </entry>"""


def paper(identifier):
    return ArxivPaper(
        identifier, 2, "Example", ("Example Author",), date(2026, 11, 25),
        date(2026, 11, 28), "Abstract", ("cs.LG",),
    )


class ArxivTests(unittest.TestCase):
    def test_parse_revision_and_withdrawal_metadata(self):
        _, _, records = _parse_feed(feed(entry("This paper has been withdrawn."), total=1))
        record = records[0]
        self.assertEqual(record.arxiv_id, "2611.00001")
        self.assertEqual(record.version, 2)
        self.assertEqual(record.title, "Weights & Computation")
        self.assertEqual(record.first_submitted, date(2026, 11, 26))
        self.assertEqual(record.doi, "10.1234/test")
        self.assertEqual(record.journal_ref, "Example Proceedings")
        self.assertTrue(record.withdrawn)
        self.assertFalse(_parse_feed(feed(entry("Revised experiments"), total=1))[2][0].withdrawn)

    def test_error_entry_is_not_an_empty_search(self):
        error = "<entry><id>http://arxiv.org/api/errors#bad</id><title>Error</title></entry>"
        with self.assertRaises(ArxivError):
            _parse_feed(feed(error, total=1))
        with self.assertRaises(ArxivError):
            _parse_feed(b"<html>unexpected response</html>")

    def test_search_pages_and_constrains_submit_dates(self):
        client = ArxivClient()
        first = paper("2611.00001")
        second = paper("2611.00002")
        start, end = date(2026, 11, 24), date(2026, 11, 28)
        with patch("scripts.wsp_arxiv.PAGE_SIZE", 1), patch.object(
            client, "_request", side_effect=[(2, 0, [first]), (2, 1, [second])]
        ) as request:
            self.assertEqual(client.search(start, end), [first, second])
        self.assertEqual([call.args[0]["start"] for call in request.call_args_list], [0, 1])
        query = request.call_args.args[0]["search_query"]
        self.assertIn("submittedDate:[202611240000 TO 202611282359]", query)
        self.assertIn('ti:"weight-space programming"', query)
        self.assertIn('abs:"direct weight editing"', query)

    def test_search_distinguishes_empty_and_incomplete(self):
        client = ArxivClient()
        start, end = date(2026, 11, 24), date(2026, 11, 28)
        with patch.object(client, "_request", return_value=(0, 0, [])):
            self.assertEqual(client.search(start, end), [])
        with patch.object(client, "_request", return_value=(1, 0, [])):
            with self.assertRaises(ArxivError):
                client.search(start, end)

    def test_lookup_preserves_order_and_fails_on_missing_record(self):
        client = ArxivClient()
        first = paper("2611.00001")
        second = paper("2611.00002")
        ids = [first.arxiv_id, second.arxiv_id, first.arxiv_id]
        with patch.object(client, "_request", return_value=(2, 0, [second, first])) as request:
            self.assertEqual(client.lookup(ids), [first, second])
        self.assertEqual(request.call_args.args[0]["id_list"], "2611.00001,2611.00002")
        with patch.object(client, "_request", return_value=(1, 0, [second])):
            with self.assertRaises(ArxivError):
                client.lookup(ids)
