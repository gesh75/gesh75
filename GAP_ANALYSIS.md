# Gap analysis — gesh75/gesh75

> Merge note (2026-09-20): `origin/main` was merged into this Cursor gap-scan
> branch. Unique scan/fix work from the PR is kept. Do not drop later main
> changes in other files.


Profile-README repo. Public surface is `README.md` (GitHub profile) plus leftover
`handoff/` from a prior Cloud Agent. This scan verified live URLs and claim
drift against source repos and [gesh75.github.io](https://gesh75.github.io/).
It did **not** invent product features or upgrade dependencies.

**Fixes in this PR (3, small):** delete superseded `handoff/`; correct netlog
maturity wording; add a README link-check workflow.

---

## P0

### P0-1 — Dead, unusable CLI coverage handoff (dead code + broken script)

- **Files:** `handoff/multivendor-cli-configurator/APPLY.md`,
  `handoff/multivendor-cli-configurator/fix_coverage_gaps.py`,
  `handoff/multivendor-cli-configurator/expand_thin_vendors.py`,
  `handoff/multivendor-cli-configurator/patch_yang_stack_vendors.py`,
  `handoff/multivendor-cli-configurator/cli-coverage-gaps-dff3.bundle`
- **Evidence:**
  1. Scripts crash in this repo. `ROOT` is the script’s parent-parent
     (`handoff/`), so they open `handoff/commands.json` which does not exist:

     ```
     FileNotFoundError: [Errno 2] No such file or directory: '/workspace/handoff/commands.json'
     ```

     Repro: `python3 handoff/multivendor-cli-configurator/fix_coverage_gaps.py`
  2. `git bundle verify` on `cli-coverage-gaps-dff3.bundle` fails:

     ```
     error: Repository lacks these prerequisite commits:
     error: cbe5de6cc043bea84f35600ed411f679100d7ded
     ```

     `APPLY.md` also tells the operator to `git fetch /path/to/cli-coverage-gaps-dff3.bundle`
     (placeholder path).
  3. The work already landed on the target repo:
     [multivendor-cli-configurator#5](https://github.com/gesh75/multivendor-cli-configurator/pull/5)
     (`Fix coverage gaps…`, merged 2026-08-06). Main now has evolved copies of
     the same three scripts and a **70,006**-command corpus (handoff still
     claims 69,854 → 69,967).
- **Fix:** delete `handoff/` (this PR). Do not re-apply the bundle.

---

## P1

### P1-1 — Stale netlog maturity on the profile table (correctness)

- **File:** `README.md` (netlog-ai row)
- **Evidence:** Profile said `0.6 in flight`. Source
  [netlog-ai README](https://raw.githubusercontent.com/gesh75/netlog-ai/main/README.md)
  and the live hub card both say **v0.6.0 shipped** (2026-08-29): Grok, causal
  timeline, 80 patterns, 423 tests.
- **Fix:** align wording with the hub (this PR).

### P1-2 — No CI on the public profile surface (CI)

- **File:** missing `.github/workflows/` (GitHub Actions `total_count: 0` on
  `gesh75/gesh75`)
- **Evidence:** `gh api repos/gesh75/gesh75/actions/workflows` → `0`. A docs-only
  hub can still ship a 404 and nobody notices. All README docs/GitHub URLs were
  HTTP 200 at scan time; that is luck, not a gate.
- **Fix:** add `scripts/check_readme_links.py` + `.github/workflows/links.yml`
  (this PR). LinkedIn is skipped: `curl` gets HTTP 999 (bot block), not proof
  the profile is gone.

### P1-3 — Claim drift has no sync process (docs / correctness)

- **File:** `README.md` vs [gesh75.github.io](https://gesh75.github.io/) (separate
  repo `gesh75/gesh75.github.io`)
- **Evidence:** netlog “in flight” vs hub “v0.6.0 shipped” (P1-1). Counts that
  *do* still match today (spot-checked 2026-09-05): Argus **315** tests, netlog
  **423** / **80** patterns, CLI **70,000+** / **17** vendors, Aegis **v0.2.0** /
  **11** frameworks / `aegis1.` tokens (`docs/PHASES.md`), skill-lint **v0.5** /
  **99** documented checks / **22-skill** NetOps pack, lab portal **69 MCP tools**.
- **Skip:** do not add a cross-repo crawler here. Next agent job should live on
  the hub repo.

---

## P2

### P2-1 — Extra public repos not on the profile table (docs)

`netbox-mcp-server` and `claude-skills` are public and recently updated; the
hub still says “Nine public labs” and lists the same nine as this README.
Adding them is a product/copy decision, not a silent fix.

### P2-2 — Foreign-repo description drift (docs)

`multivendor-ai-network-lab` GitHub **description** says “68 MCP tools”; the
live portal and that repo’s README say **69**. Out of scope for this repo.

### P2-3 — No `SECURITY.md` / `CODEOWNERS` / Dependabot (security / DX)

Expected for an application repo; low value on a two-file profile README.
No secret smells in tracked files (handoff “SECRET” strings were CLI
*examples*, now deleted).

### P2-4 — LinkedIn / X not machine-verifiable (docs)

`https://www.linkedin.com/in/gesh75` → HTTP 999 to `curl`.
`https://x.com/gesh755` and `https://x.com/gesh75` both return 200 (X serves a
shell for unknown handles). Do not “fix” social URLs without a human check.

### P2-5 — No `.gitignore` (DX)

Nothing to ignore after `handoff/` deletion. Skip.

---

## Verified non-gaps

| Check | Result |
|---|---|
| 10 GitHub Pages URLs in README | HTTP 200 |
| 9 project repo URLs | HTTP 200 |
| CLI `/`, `/docs/`, `/studio.html` | HTTP 200 |
| LICENSE | MIT, 2026, present |
| Dependency / backend work | N/A — no app code |

---

## Out of scope (skipped)

Large rewrites, dependency upgrades, cloning/running the nine product labs,
editing `gesh75.github.io`, re-opening CLI coverage, new profile widgets.
