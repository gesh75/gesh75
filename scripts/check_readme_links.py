#!/usr/bin/env python3
"""HEAD-check outbound URLs in README.md. Skip known social bot-walls."""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SKIP_HOSTS = ("linkedin.com", "www.linkedin.com", "x.com", "twitter.com")
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")


def urls_from(text: str) -> list[str]:
    seen: list[str] = []
    for raw in URL_RE.findall(text):
        url = raw.rstrip(".,;:")
        if url not in seen:
            seen.append(url)
    return seen


def host_of(url: str) -> str:
    return urllib.request.urlparse(url).hostname or ""


def check(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "gesh75-linkcheck/1"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.url
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405, 999):
            get_req = urllib.request.Request(url, method="GET", headers={"User-Agent": "gesh75-linkcheck/1"})
            try:
                with urllib.request.urlopen(get_req, timeout=15) as resp:
                    return resp.status, resp.url
            except urllib.error.HTTPError as exc2:
                return exc2.code, url
        return exc.code, url
    except Exception as exc:  # noqa: BLE001 — report any transport failure
        return 0, f"{type(exc).__name__}: {exc}"


def main() -> int:
    urls = urls_from(README.read_text())
    if not urls:
        print("no URLs found in README.md", file=sys.stderr)
        return 1
    failed = 0
    for url in urls:
        host = host_of(url)
        if any(host == h or host.endswith("." + h) for h in SKIP_HOSTS):
            print(f"SKIP {url}")
            continue
        status, detail = check(url)
        ok = 200 <= status < 400
        print(f"{'OK  ' if ok else 'FAIL'} {status} {url}" + (f" -> {detail}" if detail != url else ""))
        if not ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
