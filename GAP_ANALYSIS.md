# Gap analysis — `gesh75/gesh75`

Profile README + leftover handoff. Scanned 2026-09-05 against `main` at `d75e8a7`.

This repo is the public GitHub profile hub. There is no application runtime here. Gaps below are limited to **correctness of published claims**, **CI**, **security smell**, **DX**, **docs**, and **dead code**.

## Method (what was proved)

| Check | Result |
|---|---|
| Tree | `README.md`, `LICENSE`, `handoff/multivendor-cli-configurator/{APPLY.md,*.py,*.bundle}` — no `.github/`, no tests, no `.gitignore` |
| README outbound HTTP | All GitHub + `gesh75.github.io` URLs returned **200** (follow redirects) |
| Social | LinkedIn `https://www.linkedin.com/in/gesh75` returned **999** (bot wall, not a confirmed 404). X `https://x.com/gesh755` returned **200** |
| Live hub | `https://gesh75.github.io/` lists the same nine labs as the README table |
| Target repos | `netlog-ai` README: **v0.6.0 shipped 2026-08-29**, 423 tests. CLI configurator already has `scripts/fix_coverage_gaps.py` (6101 bytes) and merged PRs **#5** + **#6** |
| Handoff scripts in this tree | `python3 *.py --dry-run` → `FileNotFoundError` for `/workspace/handoff/commands.json` and `/workspace/handoff/index.html` |
| Bundle | `git bundle verify handoff/multivendor-cli-configurator/cli-coverage-gaps-dff3.bundle` fails here (missing prerequisite `cbe5de6`). That commit exists on `gesh75/multivendor-cli-configurator`, and the work already landed as PR #5 |
| Secrets | No live keys/tokens. `SECRET` strings in the handoff CLI samples are placeholders |
| GitHub metadata | `gh api repos/gesh75/gesh75/contents/.github` → **404**. Repo `homepage` is empty; `has_pages` is false (expected — hub lives in `gesh75/gesh75.github.io`) |

## P0

### P0-1 — Profile README still says netlog-ai 0.6 is “in flight”

- **Area:** correctness / docs
- **File:** [`README.md`](README.md) (netlog-ai row)
- **Evidence:** README text is `0.6 in flight`. The live hub (`https://gesh75.github.io/`) says **“v0.6.0 shipped”**. Upstream [`gesh75/netlog-ai` README](https://github.com/gesh75/netlog-ai/blob/main/README.md) says **“v0.6.0 (2026-08-29) ships the causal console”** with 423 tests. The profile is the first thing visitors see and it is stale.
- **Smallest fix:** Change the blurb to shipped v0.6.0. Do not invent a new product row.

### P0-2 — Handoff APPLY path is stale and the scripts are not runnable here

- **Area:** correctness / docs / dead code / broken script
- **Files:**
  - [`handoff/multivendor-cli-configurator/APPLY.md`](handoff/multivendor-cli-configurator/APPLY.md)
  - [`handoff/multivendor-cli-configurator/fix_coverage_gaps.py`](handoff/multivendor-cli-configurator/fix_coverage_gaps.py)
  - [`handoff/multivendor-cli-configurator/expand_thin_vendors.py`](handoff/multivendor-cli-configurator/expand_thin_vendors.py)
  - [`handoff/multivendor-cli-configurator/patch_yang_stack_vendors.py`](handoff/multivendor-cli-configurator/patch_yang_stack_vendors.py)
  - `handoff/multivendor-cli-configurator/cli-coverage-gaps-dff3.bundle`
- **Evidence:**
  1. APPLY.md still says the agent **cannot push** and lists **Apply (preferred)** as if the work is pending.
  2. The work already merged on the target: [multivendor-cli-configurator#5](https://github.com/gesh75/multivendor-cli-configurator/pull/5) (`886ba61`, 2026-08-06). Follow-up [#6](https://github.com/gesh75/multivendor-cli-configurator/pull/6) evolved the same scripts further.
  3. Local `fix_coverage_gaps.py` is **4713 bytes**; target `scripts/fix_coverage_gaps.py` is **6101 bytes** (STP/BFD/LACP promotion). Re-applying this snapshot would regress the target.
  4. APPLY.md tells the reader to `git fetch /path/to/cli-coverage-gaps-dff3.bundle` — placeholder path. The bundle sits next to APPLY.md.
  5. Running the scripts from this repo:

     ```
     FileNotFoundError: ... '/workspace/handoff/commands.json'
     FileNotFoundError: ... '/workspace/handoff/index.html'
     ```

     They resolve `ROOT = Path(__file__).parent.parent`, which is `handoff/`, not a CLI corpus checkout.
- **Smallest fix:** Mark the handoff APPLIED and delete the stale script/bundle copies. Live copies live in the target repo.

### P0-3 — No CI; the only public artifact has no regression gate

- **Area:** CI / missing test
- **File:** missing `.github/workflows/` — `GET /repos/gesh75/gesh75/contents/.github` returned **404**
- **Evidence:** This repo’s job is outbound links + version claims. There is no workflow, no link check, and no test that would have caught P0-1. A profile hub that can ship a stale or 404 link with zero signal is a P0 process gap, not a product gap.
- **Smallest fix:** One workflow that HEAD-checks README URLs (skip LinkedIn/X bot walls).

## P1

### P1-1 — GitHub repo homepage / topics are empty

- **Area:** DX / docs
- **Evidence:** `gh api repos/gesh75/gesh75 --jq '{homepage,topics}'` → `homepage: null`, `topics: []`. The hub URL `https://gesh75.github.io/` is already in the README. Setting About → Website would surface it on the profile card. Out of band for a file PR (repo settings).

### P1-2 — CLI docs column points at the cheatsheet, not the docs page

- **Area:** docs
- **File:** [`README.md`](README.md) CLI row → `https://gesh75.github.io/multivendor-cli-configurator/`
- **Evidence:** Both that URL and `/docs/` and `/studio.html` return 200. The target README leads with `/docs/` for architecture and a separate Studio link. Not broken — just thinner than the hub. Leave unless a later pass wants a second docs link.

### P1-3 — No local “how to check this README” script

- **Area:** DX
- **Evidence:** No `Makefile`, no `scripts/`, no contributor note. A one-file link checker (same as P0-3) covers this.

## P2

### P2-1 — No `.gitignore`

- **Area:** DX
- **Evidence:** Running the handoff scripts created `handoff/.../__pycache__/` (untracked). A two-line gitignore is enough. Not a correctness bug.

### P2-2 — Social links are not CI-checkable

- **Area:** CI / docs
- **Evidence:** LinkedIn 999 from this environment. Do not fail CI on it. Treat as a manual check.

### P2-3 — Handoff CLI samples used literal `SECRET` / `public` community strings

- **Area:** security (smell only)
- **File:** `expand_thin_vendors.py` (RADIUS `secret \"SECRET\"`, SNMP `public`)
- **Evidence:** Placeholder lab strings, not credentials. Still, they should not be re-copied forward as if they were real. Deleting the stale copies removes the smell from this repo.

### P2-4 — No issue templates / CODEOWNERS / topics

- **Area:** DX
- **Evidence:** `gh issue list --repo gesh75/gesh75` is empty; issues are enabled. Fine for a profile repo. Skip unless traffic appears.

## Skipped (on purpose)

- Dependency upgrades — none exist.
- New product features, backend, or a docs-site rewrite — hub lives in `gesh75/gesh75.github.io`.
- Re-applying the CLI coverage bundle to the target repo — already merged and superseded.
- Changing GitHub About/homepage via API — settings, not a tree change.
- Inventing tests for the handoff Python — those files are the wrong tree.

## Fixes in this PR (cap: 3)

1. **README** — netlog-ai blurb: in flight → shipped v0.6.0 (P0-1).
2. **Handoff** — APPLY.md marked APPLIED; stale scripts + bundle deleted (P0-2, P2-3).
3. **CI** — `scripts/check_readme_links.py` + `.github/workflows/linkcheck.yml` (P0-3, P1-3). `.gitignore` is a two-line companion so `__pycache__` cannot sneak in.

## Next recommended agent job

Open a Cloud Agent on `gesh75/gesh75.github.io` (or a scheduled profile-sync check) that diffs this README’s version/test-count blurbs against the live hub cards so claims cannot drift again.
