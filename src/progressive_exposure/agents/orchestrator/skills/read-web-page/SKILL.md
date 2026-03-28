---
name: read-web-page
description: Fetches and extracts readable content from a web page given a URL. Use when the user asks to read, summarize, or extract information from a website, URL, or web page. Handles HTML parsing, text extraction, and returns clean readable text.
metadata:
  author: progressive-exposure
  version: "1.0"
---

# Read Web Page

## When to use this skill

Use this skill when the user needs to:
- Read or fetch content from a URL or web page
- Extract text from a website
- Summarize or analyze web page content
- Scrape readable text from an HTML page

## How it works

1. The user provides a URL to read
2. The script fetches the page content via HTTP
3. HTML is parsed and non-content elements (scripts, styles, nav, etc.) are removed
4. Clean, readable text is extracted and returned

## Usage

When the user requests to read or fetch a web page:
1. Run the `scripts/fetch_page.py` script with `--url <URL>` (e.g. `--url https://example.com`)
2. Present the extracted content to the user

## Output format

The script outputs:
- **Title**: The page title (if available)
- **URL**: The fetched URL
- **Content**: The extracted readable text, with headings preserved as Markdown-style headers

## Error handling

- If the URL is unreachable, the script prints an error message and exits with code 1
- If the page has no extractable content, it reports that the page appears empty
- Timeouts are set to 30 seconds

## Dependencies

The script uses only Python standard library modules (urllib and html.parser), so no additional packages are required.

## Guidelines

- Always provide a full URL including the scheme (e.g., `https://`)
- The script respects a 30-second timeout for requests
- Very large pages will have their content truncated to keep output manageable
- The script sets a standard User-Agent header to avoid being blocked
