---
name: surge-config-guard
description: Use when inspecting, editing, troubleshooting, validating, or reloading Surge for macOS profiles, policy groups, rules, DNS, MITM, proxy routing, or surge-cli behavior. Always use for requests involving Surge configuration changes, proxy strategy changes, Comet/Perplexity routing through Surge, rule ordering, profile recovery, or avoiding invalid Surge edits.
---

# Surge Config Guard

## Purpose

Use this skill for every Surge profile change. The priority is to keep Surge loadable, preserve the user's working network, and prove changes with `surge-cli` before declaring success.

Official docs to consult when needed:

- Knowledge base: https://kb.nssurge.com/surge-knowledge-base
- Manual: https://manual.nssurge.com/
- Configuration: https://manual.nssurge.com/overview/configuration.html
- Policy groups and external policies: https://manual.nssurge.com/policy-group/policy-including.html

## Mandatory Workflow

1. Identify the active profile before editing.
   - Prefer `lsof -c Surge | rg 'Profiles|\\.conf'`.
   - Also inspect `surge-cli --raw dump profile original` when Surge is running.
   - Do not assume a filename from the user's wording.

2. Read relevant profile sections first.
   - Use `rg`/`sed` for `[General]`, `[Proxy]`, `[Proxy Group]`, `[Rule]`, `[MITM]`, and related lines.
   - Check currently effective rules with `surge-cli dump rule`.

3. Back up the exact profile file before any edit.
   - Backup name pattern: `<profile>.bak-YYYYMMDD-HHMMSS-<reason>`.
   - Never overwrite older backups.

4. Edit narrowly.
   - Use `apply_patch` for manual edits.
   - Keep unrelated formatting and certificate blobs intact.
   - Do not rewrite the whole profile unless the user explicitly asks.

5. Reload and validate immediately.
   - Run `surge-cli reload`.
   - Run `surge-cli dump rule` for rule-order checks.
   - Run `surge-cli --raw dump profile original` to confirm Surge ingested the modified profile.
   - Run `surge-cli --raw dump event` and inspect recent errors/warnings.

6. If reload fails, roll back immediately.
   - Restore the newest backup made for this change.
   - Reload again and verify the profile is loadable.
   - Tell the user exactly what failed.

## Hard Safety Rules

- Never place runtime proxy names discovered from request logs into a source profile unless they are explicitly defined in `[Proxy]` or are valid members exposed to the profile syntax.
- External `policy-path` imported nodes may appear in logs, but source profiles often cannot reference those concrete node names directly. Prefer referencing existing source-level groups such as region groups or select groups.
- Surge smart groups should not be treated as fixed egress. If a service needs a stable IP/session, prefer a valid source-level select group or a documented fixed policy that Surge accepts.
- Do not enable `hijack-dns`, MITM hostnames, or rewrite/scripting changes as a casual stability tweak. These can alter large traffic surfaces.
- Do not remove the user's paid/custom DoH or subscription URLs unless explicitly requested.
- Do not expose secrets from `ca-p12`, subscription URLs, or private DoH URLs in final answers. Summarize instead.
- If a change touches `[MITM]`, certificate data, `[Script]`, `[Rewrite]`, or subscription URLs, be extra conservative and validate with both `dump profile` and `dump event`.

## Common Commands

```bash
SURGE_CLI="/Applications/Surge.app/Contents/Applications/surge-cli"
PROFILE="$HOME/Library/Application Support/Surge/Profiles/profile.conf"

lsof -c Surge 2>/dev/null | rg 'Profiles|\\.conf'
"$SURGE_CLI" reload
"$SURGE_CLI" dump rule | sed -n '1,120p'
"$SURGE_CLI" environment
"$SURGE_CLI" --raw dump profile original
"$SURGE_CLI" --raw dump event
"$SURGE_CLI" --raw dump request
"$SURGE_CLI" flush dns
```

For repeatable validation, use `scripts/surge_guard.sh`.

## Change Patterns

For low-risk stability tuning, prefer small `[General]` edits such as `test-timeout`, `dns-server`, `skip-proxy`, and `always-real-ip`, then reload and verify.

For service-specific routing, place domain/process rules before broad rule-sets only when needed, and confirm the effective order with `dump rule`.

For troubleshooting, compare:

- source profile file on disk
- `surge-cli --raw dump profile original`
- `surge-cli dump rule`
- recent `dump request` entries for process/rule/policy/failed/rejected

Only report a fix as done when the effective profile and rules match the intended change.
