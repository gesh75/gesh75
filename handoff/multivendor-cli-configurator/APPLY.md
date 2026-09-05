# Coverage-gap handoff — APPLIED

Do **not** re-apply anything from this folder.

The coverage-gap work that used to live here landed on
[`gesh75/multivendor-cli-configurator#5`](https://github.com/gesh75/multivendor-cli-configurator/pull/5)
(merged 2026-08-06, `886ba61`). Follow-up
[`#6`](https://github.com/gesh75/multivendor-cli-configurator/pull/6)
evolved the same scripts further (STP/BFD/LACP promotion).

Live copies (run only inside that repo):

- `scripts/fix_coverage_gaps.py`
- `scripts/expand_thin_vendors.py`
- `scripts/patch_yang_stack_vendors.py`

This profile repo is not the CLI corpus. The snapshot scripts and
incremental git bundle were deleted so nobody re-runs an older copy
against `handoff/commands.json` (that path does not exist) or regresses
the target.
