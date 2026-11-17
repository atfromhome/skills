# Tracker issue #210: Donation report CSV export — spec

**Labels:** spec, verification:b
**Level:** B. No formal gate (level B).
**Seams:** the CSV encoder and the export endpoint of the donations report. Commands (from AGENTS.md): typecheck `make typecheck` · single test `go test ./internal/report/... -run <Name>` · full suite `make test` · properties `go test ./internal/report/... -run Prop`

### Properties
- PROP-1: parsing the exported CSV gives back exactly the report rows, for any filter.
- PROP-2: the sum of the amount column equals the report total, for any filter.
- PROP-3: no cell starts with =, +, - or @ unless prefixed with an apostrophe.

## Tickets (sub-issues)
- #211 Donation report CSV export 01 — property tests and rapid. **Closed**, merged into `donation-report-csv-export/integration` (PR #216). PROP-1..3 are in the repo; PROP-1 and PROP-3 are pending (`t.Skip("ticket 02")`), PROP-2 is pending (`t.Skip("ticket 03")`).
- #212 Donation report CSV export 02 — CSV encoder with formula escaping. Open, unassigned. Blocked by #211 (closed). Owns PROP-1, PROP-3.
- #213 Donation report CSV export 03 — export endpoint honours the report filters. Open, unassigned. Blocked by #211 (closed). Owns PROP-2.
- #214 Donation report CSV export 04 — Export button on the report page. Open, unassigned. Blocked by #212 and #213.

## Branches and PRs
- Integration branch `donation-report-csv-export/integration`, tip `7a1c0e3` (contains ticket 01).
- Draft PR #217 from the integration branch to `main`, opened after ticket 01 merged. Body lists `Closes #211 … #214`.
