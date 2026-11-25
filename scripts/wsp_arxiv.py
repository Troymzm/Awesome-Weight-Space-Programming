"""Incremental arXiv search and catalog refresh via the public Atom API."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from http.client import HTTPException
import re
from time import monotonic, sleep
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree


API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
SEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
ARTICLE_ID = r"(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})"
ENTRY_ID = re.compile(rf"https?://(?:www\.)?arxiv\.org/abs/({ARTICLE_ID})v([1-9]\d*)")
WITHDRAWN = re.compile(
    r"^(?:\[(?:withdrawn|retracted)\]|(?:withdrawn|retracted)(?:\b.*)?$|"
    r"(?:this|the) (?:paper|article|submission|manuscript|preprint) "
    r"(?:has (?:now )?been|was|is(?: being)?) (?:withdrawn|retracted)\b)",
    re.IGNORECASE,
)
CORE_PHRASES = (
    "weight-space programming",
    "weight space programming",
    "program-to-weight compilation",
    "LLM-written weights",
    "Self-WSP",
)
DISCOVERY_PHRASES = (
    "weights by hand",
    "writing neural network weights",
    "gradient-free weight editing",
    "agentic weight editing",
    "agentic coding",
    "direct weight editing",
    "weight-space repair",
    "rewriting its weights",
    "rewrite their own weights",
)
CATEGORIES = ("cs.AI", "cs.CL", "cs.CV", "cs.LG", "cs.PL", "cs.RO", "stat.ML")
PAGE_SIZE = 100
BATCH_SIZE = 50
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}


class ArxivError(RuntimeError):
    """An API error, malformed record, or incomplete result set."""


@dataclass(frozen=True)
class ArxivPaper:
    arxiv_id: str
    version: int
    title: str
    authors: tuple[str, ...]
    first_submitted: date
    updated: date
    abstract: str
    categories: tuple[str, ...]
    doi: str = ""
    journal_ref: str = ""
    comment: str = ""
    withdrawn: bool = False


def _text(element, tag):
    return " ".join((element.findtext(tag) or "").split())


def _parse_date(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return result.astimezone(timezone.utc).date()


def _parse_entry(entry):
    identifier = _text(entry, ATOM + "id")
    title = _text(entry, ATOM + "title")
    abstract = _text(entry, ATOM + "summary")
    comment = _text(entry, ARXIV + "comment")
    if title == "Error" or "/api/errors" in identifier:
        raise ArxivError("arXiv returned an API error entry")

    match = ENTRY_ID.fullmatch(identifier)
    authors = tuple(_text(node, ATOM + "name") for node in entry.findall(ATOM + "author"))
    if not match or not title or not authors or not all(authors):
        raise ArxivError("arXiv entry is missing a versioned identifier, title, or author")
    arxiv_id, version = match.groups()
    try:
        first_submitted = _parse_date(_text(entry, ATOM + "published"))
        updated = _parse_date(_text(entry, ATOM + "updated"))
    except ValueError as error:
        raise ArxivError(f"arXiv:{arxiv_id} has an invalid timestamp") from error
    if updated < first_submitted:
        raise ArxivError(f"arXiv:{arxiv_id} has inconsistent timestamps")

    return ArxivPaper(
        arxiv_id=arxiv_id,
        version=int(version),
        title=title,
        authors=authors,
        first_submitted=first_submitted,
        updated=updated,
        abstract=abstract,
        categories=tuple(node.get("term", "") for node in entry.findall(ATOM + "category")),
        doi=_text(entry, ARXIV + "doi"),
        journal_ref=_text(entry, ARXIV + "journal_ref"),
        comment=comment,
        withdrawn=any(WITHDRAWN.search(value) for value in (title, comment, abstract)),
    )


def _parse_feed(data):
    try:
        feed = ElementTree.fromstring(data)
        if feed.tag != ATOM + "feed":
            raise ValueError("expected an Atom feed")
        total = int(_text(feed, SEARCH + "totalResults"))
        start = int(_text(feed, SEARCH + "startIndex"))
        if total < 0 or start < 0:
            raise ValueError("negative result metadata")
    except (ElementTree.ParseError, ValueError) as error:
        raise ArxivError("arXiv returned an invalid Atom feed") from error
    return total, start, [_parse_entry(entry) for entry in feed.findall(ATOM + "entry")]


def _search_query(start, end):
    def phrases(group):
        return " OR ".join(f'{field}:"{term}"' for term in group for field in ("ti", "abs"))

    categories = " OR ".join(f"cat:{category}" for category in CATEGORIES)
    dates = f"submittedDate:[{start:%Y%m%d}0000 TO {end:%Y%m%d}2359]"
    return f"(({phrases(CORE_PHRASES)}) OR (({phrases(DISCOVERY_PHRASES)}) AND ({categories}))) AND {dates}"


def _retry_after(header):
    if not header:
        return 0
    if header.isdecimal():
        return int(header)
    try:
        expiry = parsedate_to_datetime(header)
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        return max(0, (expiry - datetime.now(timezone.utc)).total_seconds())
    except (TypeError, ValueError):
        return 0


class ArxivClient:
    """Run queries serially under arXiv's API request rate limit."""

    def __init__(self):
        self._next_request = 0.0

    def _request(self, params):
        url = f"{API}?{urlencode(params)}"
        request = Request(
            url,
            headers={
                "Accept": "application/atom+xml",
                "User-Agent": "Awesome-Weight-Space-Programming weekly literature index",
            },
        )
        for attempt in range(3):
            delay = self._next_request - monotonic()
            if delay > 0:
                sleep(delay)
            self._next_request = monotonic() + 3.0
            try:
                with urlopen(request, timeout=30) as response:
                    data = response.read(MAX_RESPONSE_BYTES + 1)
                if len(data) > MAX_RESPONSE_BYTES:
                    raise ArxivError("arXiv response exceeded the size limit")
                return _parse_feed(data)
            except HTTPError as error:
                retry_after = _retry_after(error.headers.get("Retry-After"))
                error.close()
                if attempt == 2 or error.code not in RETRYABLE_STATUS:
                    raise ArxivError(f"arXiv returned HTTP {error.code}") from error
            except (OSError, HTTPException) as error:
                if attempt == 2:
                    raise ArxivError("arXiv request failed after retries") from error
                retry_after = 0
            if retry_after > 60:
                raise ArxivError("arXiv requested a retry after more than 60 seconds")
            self._next_request = max(self._next_request, monotonic() + max(3 * (2**attempt), retry_after))

    def search(self, start: date, end: date) -> list[ArxivPaper]:
        """Find papers first submitted in the inclusive UTC date range."""
        if start > end:
            raise ValueError("search start follows search end")
        query = _search_query(start, end)
        papers = {}
        offset = 0
        expected_total = None
        while True:
            total, page_start, page = self._request(
                {
                    "search_query": query,
                    "start": offset,
                    "max_results": PAGE_SIZE,
                    "sortBy": "submittedDate",
                    "sortOrder": "ascending",
                }
            )
            if total > 30_000:
                raise ArxivError("arXiv search exceeded the API limit for a query")
            if page_start != offset or (expected_total is not None and total != expected_total):
                raise ArxivError("arXiv search changed while paging")
            if len(page) != min(PAGE_SIZE, total - offset):
                raise ArxivError("arXiv returned an incomplete search page")
            for paper in page:
                if paper.arxiv_id in papers or not start <= paper.first_submitted <= end:
                    raise ArxivError("arXiv returned a duplicate or out-of-window search record")
                papers[paper.arxiv_id] = paper
            offset += len(page)
            if offset == total:
                return list(papers.values())
            expected_total = total

    def lookup(self, ids: Iterable[str]) -> list[ArxivPaper]:
        """Retrieve the latest versions of the specified unversioned arXiv IDs."""
        unique = list(dict.fromkeys(ids))
        if any(not re.fullmatch(ARTICLE_ID, identifier) for identifier in unique):
            raise ValueError("arXiv lookup requires unversioned identifiers")
        papers = {}
        for start in range(0, len(unique), BATCH_SIZE):
            batch = unique[start : start + BATCH_SIZE]
            total, offset, page = self._request({"id_list": ",".join(batch), "max_results": len(batch)})
            found = {paper.arxiv_id: paper for paper in page}
            if offset != 0 or total != len(page) or len(page) != len(found) or found.keys() != set(batch):
                raise ArxivError(
                    f"arXiv lookup did not return all requested IDs in batch starting at {batch[0]}"
                )
            papers.update(found)
        return [papers[identifier] for identifier in unique]
