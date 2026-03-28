#!/usr/bin/env python3
"""Fetch a web page and extract readable text content.

Usage:
    python fetch_page.py --url <URL>

Outputs clean, readable text extracted from the HTML page.
Uses only Python standard library modules.
"""

import argparse
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urlparse

MAX_CONTENT_LENGTH = 100_000  # characters
REQUEST_TIMEOUT = 30  # seconds
USER_AGENT = "Mozilla/5.0 (compatible; ReadWebPageSkill/1.0)"


class TextExtractor(HTMLParser):
    """HTML parser that extracts readable text, converting headings to Markdown."""

    SKIP_TAGS = frozenset(
        [
            "script",
            "style",
            "noscript",
            "iframe",
            "svg",
            "math",
            "nav",
            "footer",
            "header",
            "aside",
            "form",
        ]
    )

    HEADING_TAGS = frozenset(["h1", "h2", "h3", "h4", "h5", "h6"])

    BLOCK_TAGS = frozenset(
        [
            "p",
            "div",
            "section",
            "article",
            "main",
            "blockquote",
            "li",
            "tr",
            "br",
            "hr",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ]
    )

    def __init__(self) -> None:
        super().__init__()
        self.result: list[str] = []
        self.skip_depth: int = 0
        self.current_tag: str | None = None
        self.title: str = ""
        self._in_title: bool = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()

        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return

        if self.skip_depth > 0:
            return

        if tag == "title":
            self._in_title = True
            self._title_parts = []

        if tag in self.BLOCK_TAGS:
            self.result.append("\n")

        if tag in self.HEADING_TAGS:
            level = int(tag[1])
            self.result.append("#" * level + " ")

        self.current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return

        if tag == "title":
            self._in_title = False
            self.title = "".join(self._title_parts).strip()

        if tag in self.BLOCK_TAGS:
            self.result.append("\n")

        self.current_tag = None

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)

        if self.skip_depth > 0:
            return

        text = data.strip()
        if text:
            self.result.append(text + " ")

    def get_text(self) -> str:
        raw = "".join(self.result)
        # Collapse excessive whitespace
        lines = raw.split("\n")
        cleaned: list[str] = []
        prev_blank = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if not prev_blank:
                    cleaned.append("")
                prev_blank = True
            else:
                cleaned.append(stripped)
                prev_blank = False
        return "\n".join(cleaned).strip()


def fetch_page(url: str) -> tuple[str, str]:
    """Fetch a URL and return (title, extracted_text)."""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            html_bytes = response.read()
            html = html_bytes.decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} when fetching {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not reach {url} — {e.reason}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError:
        print(
            f"Error: Request to {url} timed out after {REQUEST_TIMEOUT}s",
            file=sys.stderr,
        )
        sys.exit(1)

    extractor = TextExtractor()
    extractor.feed(html)
    title = extractor.title
    text = extractor.get_text()

    if len(text) > MAX_CONTENT_LENGTH:
        text = (
            text[:MAX_CONTENT_LENGTH] + "\n\n[Content truncated at 100,000 characters]"
        )

    return title, text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch a web page and extract readable text content.",
    )
    parser.add_argument(
        "--url", type=str, required=True, help="The URL of the web page to fetch."
    )
    args = parser.parse_args()

    url = args.url
    title, text = fetch_page(url)

    print(f"# {title}" if title else "# (No title)")
    print(f"**URL:** {url}")
    print()

    if text:
        print(text)
    else:
        print("(Page appears to have no extractable text content.)")


if __name__ == "__main__":
    main()
