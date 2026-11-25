"""Incremental arXiv search and exact-version status verification."""

from collections.abc import Iterable
from dataclasses import dataclass, replace
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from http.client import HTTPException
import re
from time import monotonic, sleep
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from xml.etree import ElementTree


API = "https://export.arxiv.org/api/query"
ABS = "https://arxiv.org/abs"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
SEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
ARTICLE_ID = r"(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})"
ENTRY_ID = re.compile(rf"https?://(?:www\.)?arxiv\.org/abs/({ARTICLE_ID})v([1-9]\d*)")
VERSION_LINE = re.compile(r"^\[v([1-9]\d*)\]\s+(.+)$")
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
    "weights as programs",
    "programming model weights",
)
WEIGHT_SPACE_TITLES = ("in weight space", "in the weight space", "in weight-space", "from weights")
OPERATION_TERMS = (
    "read", "reads", "reading", "write", "writes", "writing", "repair", "repairing",
    "edit", "editing", "diagnose", "diagnosing", "programming", "synthesis",
)
CATEGORIES = ("cs.AI", "cs.CL", "cs.CV", "cs.LG", "cs.PL", "cs.RO", "stat.ML")
PAGE_SIZE = 100
BATCH_SIZE = 50
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}
ABS_CRAWL_DELAY = 15


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
    withdrawn: bool | None = None


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
    space = " OR ".join(f'ti:"{term}"' for term in WEIGHT_SPACE_TITLES)
    operations = " OR ".join(f"ti:{term}" for term in OPERATION_TERMS)
    exploration = f"({phrases(DISCOVERY_PHRASES)}) OR (({space}) AND ({operations}))"
    dates = f"submittedDate:[{start:%Y%m%d}0000 TO {end:%Y%m%d}2359]"
    return f"(({phrases(CORE_PHRASES)}) OR (({exploration}) AND ({categories}))) AND {dates}"


class _VersionPage(HTMLParser):
    """Read the submission history and arXiv's own download controls."""

    def __init__(self):
        super().__init__()
        self.history_depth = 0
        self.history = []
        self.selected = []
        self.version_label = None
        self.version_linked = False
        self.downloads = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if tag == "div" and (self.history_depth or "submission-history" in classes):
            self.history_depth += 1
        if self.history_depth:
            if tag == "br":
                self.history.append("\n")
            if tag == "strong":
                self.version_label = []
                self.version_linked = False
            if tag == "a" and self.version_label is not None:
                self.version_linked = True
        full_text = {"download-pdf", "mobile-submission-download", "download-eprint"}
        if tag == "a" and full_text.intersection(classes) and attrs.get("href"):
            self.downloads.append(attrs["href"])

    def handle_endtag(self, tag):
        if self.history_depth and tag == "div":
            self.history_depth -= 1
        if tag == "strong" and self.version_label is not None:
            if not self.version_linked:
                self.selected.append(" ".join(self.version_label))
            self.version_label = None

    def handle_data(self, data):
        if self.history_depth:
            self.history.append(data.strip())
            if self.version_label is not None:
                self.version_label.append(data.strip())


def _withdrawn_status(data, final_url, paper):
    expected = f"{paper.arxiv_id}v{paper.version}"
    match = ENTRY_ID.fullmatch(final_url)
    if not final_url.startswith("https://") or not match or match.groups() != (paper.arxiv_id, str(paper.version)):
        raise ArxivError(f"arXiv did not serve the requested abstract page for {expected}")

    page = _VersionPage()
    try:
        page.feed(data.decode("utf-8"))
        page.close()
        versions = [m for line in " ".join(page.history).split("\n")
                    if (m := VERSION_LINE.fullmatch(" ".join(line.split())))]
        matches = [m[2] for m in versions if m[1] == str(paper.version)]
        if (page.history_depth or " ".join(page.selected).strip() != f"[v{paper.version}]"
                or len(matches) != 1):
            raise ValueError("missing unique selected version")
        current = {expected}
        if paper.version == max(int(m[1]) for m in versions):
            current.add(paper.arxiv_id)
        has_download = False
        for link in page.downloads:
            parsed = urlsplit(link)
            parts = parsed.path.removeprefix("/").split("/", 1)
            if (parsed.scheme in {"", "https"} and parsed.netloc in {"", "arxiv.org", "www.arxiv.org"}
                    and len(parts) == 2
                    and parts[0] in {"pdf", "src"} and parts[1].removesuffix(".pdf") in current):
                has_download = True
                break
        withdrawn = bool(re.search(r"\((?:withdrawn|retracted)\)\s*$", matches[0], re.I))
        if withdrawn != has_download:
            return withdrawn
    except (UnicodeError, ValueError) as error:
        raise ArxivError(f"arXiv status was not verifiable for {expected}") from error
    raise ArxivError(f"arXiv status was not verifiable for {expected}")


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
        data, _ = self._get(url, "application/atom+xml", 3)
        return _parse_feed(data)

    def _get(self, url, content_type, interval):
        request = Request(
            url,
            headers={
                "Accept": content_type,
                "User-Agent": "Awesome-Weight-Space-Programming weekly literature index",
            },
        )
        for attempt in range(3):
            delay = self._next_request - monotonic()
            if delay > 0:
                sleep(delay)
            self._next_request = monotonic() + interval
            try:
                with urlopen(request, timeout=30) as response:
                    data = response.read(MAX_RESPONSE_BYTES + 1)
                    final_url = response.geturl()
                if len(data) > MAX_RESPONSE_BYTES:
                    raise ArxivError("arXiv response exceeded the size limit")
                return data, final_url
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
            self._next_request = max(self._next_request, monotonic() + max(interval, 3 * (2**attempt), retry_after))

    def check_status(self, paper: ArxivPaper) -> ArxivPaper:
        """Resolve status on the exact arXiv abstract page under its crawl delay."""
        if not re.fullmatch(ARTICLE_ID, paper.arxiv_id) or paper.version < 1:
            raise ValueError("arXiv status check requires a valid versioned identifier")
        url = f"{ABS}/{paper.arxiv_id}v{paper.version}"
        data, final_url = self._get(url, "text/html", ABS_CRAWL_DELAY)
        return replace(paper, withdrawn=_withdrawn_status(data, final_url, paper))

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
