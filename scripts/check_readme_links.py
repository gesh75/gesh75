#!/usr/bin/env python3
"""Fail if README.md HTTP(S) links do not return 2xx/3xx.

Skips hosts that block datacenter crawlers (LinkedIn 999, etc.).
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.parse
import urllib.request

README = "README.md"
SKIP_HOSTS = ("linkedin.com", "www.linkedin.com")
LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")


def main() -> int:
    text = open(README, encoding="utf-8").read()
    urls = list(dict.fromkeys(LINK_RE.findall(text)))
    if not urls:
        print("no http(s) links in README.md", file=sys.stderr)
        return 1

    failed = 0
    for url in urls:
        host = urllib.parse.urlparse(url).hostname or ""
        if host in SKIP_HOSTS or host.endswith(".linkedin.com"):
            print(f"SKIP {url}")
            continue
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "gesh75-readme-link-check"},
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                code = resp.status
        except urllib.error.HTTPError as exc:
            code = exc.code
            if code in (405, 403):
                get = urllib.request.Request(
                    url,
                    headers={"User-Agent": "gesh75-readme-link-check"},
                )
                try:
                    with urllib.request.urlopen(get, timeout=20) as resp:
                        code = resp.status
                except urllib.error.HTTPError as exc2:
                    code = exc2.code
        except Exception as exc:  # noqa: BLE001 — report and fail the URL
            print(f"FAIL {url} ({exc})")
            failed += 1
            continue
        ok = 200 <= code < 400
        print(f"{'OK  ' if ok else 'FAIL'} {code} {url}")
        if not ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
