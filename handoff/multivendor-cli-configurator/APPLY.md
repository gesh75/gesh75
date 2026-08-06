# Coverage-gap fix handoff — multivendor-cli-configurator

This Cloud Agent run is bound to `gesh75/gesh75` and **cannot push** to
`gesh75/multivendor-cli-configurator` (`cursor[bot]` → 403). All fixes were
implemented and committed locally on branch `cursor/cli-coverage-gaps-dff3`
(commit `0791ec3`).

## Apply (preferred)

1. Grant the Cursor GitHub App **write** access to `gesh75/multivendor-cli-configurator`,
   **or** start a new Cloud Agent directly on that repo.
2. Then either re-run this agent, or:

```bash
git clone https://github.com/gesh75/multivendor-cli-configurator
cd multivendor-cli-configurator
git fetch /path/to/cli-coverage-gaps-dff3.bundle cursor/cli-coverage-gaps-dff3:cursor/cli-coverage-gaps-dff3
git checkout cursor/cli-coverage-gaps-dff3
git push -u origin cursor/cli-coverage-gaps-dff3
gh pr create --base main --head cursor/cli-coverage-gaps-dff3 \
  --title "fix coverage gaps: NX-OS/VXLAN/EVPN, thin vendors, YANG stack" \
  --body "See commit message and scripts/fix_coverage_gaps.py"
```

## What shipped in the commit

| Area | Change |
|------|--------|
| Corpus | 69,854 → **69,967** commands |
| NX-OS / IOS-XE | Retagged **189** nxos · **113** iosxe (was nearly all `ios`) |
| Overlay cats | **VXLAN 255** · **EVPN 498** dedicated categories |
| Thin vendors | +113 curated cmds (SONiC, NVIDIA, Huawei, SR OS, Aruba, Extreme, …) |
| Data quality | 0 over-long titles · 4,157 placeholder unescapes · STP/VRRP collapsed |
| Automate | YANG `AUTO_*` extended to **FRR · VyOS · Nokia · Aruba**; OS-aware Netmiko/Ansible |
| Docs | README + docs/index.html + ARCHITECTURE refreshed; stress vendor_coverage updated |

## Scripts added

- `scripts/fix_coverage_gaps.py`
- `scripts/expand_thin_vendors.py`
- `scripts/patch_yang_stack_vendors.py`

Re-run order after future merges:

```bash
python3 scripts/expand_thin_vendors.py
python3 scripts/fix_coverage_gaps.py
python3 scripts/patch_yang_stack_vendors.py
python3 scripts/check_consistency.py
```
