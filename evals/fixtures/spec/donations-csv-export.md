<!-- vflow:decision-summary -->
## Decision summary: CSV export of the donations report

**Source:** grill session, 2026-11-12. **Tracker issue:** #157 Export donations report as CSV. **Confirmed by:** Rudi (finance lead), 2026-11-12.

### Problem and goal
Finance copies the donations report into a spreadsheet by hand every month to reconcile with bank statements. Done when an admin or finance user can download the report as a CSV that opens correctly in Excel and Google Sheets and matches the on-screen total.

### Settled decisions
- D1. The export contains exactly the rows the report shows under its current filters (date range, campaign, status), across all pages (Q1)
- D2. One row per donation; no subtotal or total rows (Q2)
- D3. Columns, in order: donation id, paid at, donor name, donor email, campaign, status, amount, currency (Q3)
- D4. Anonymous donations leave donor name and email empty; the export never reveals who an anonymous donor is (Q4)
- D5. Amounts are whole rupiah as plain integers with no separators or symbol; currency is its own column (Q5)
- D6. Timestamps are ISO 8601 in Asia/Jakarta with the offset (Q6)
- D7. UTF-8 with BOM, comma separated, quoted per RFC 4180; a cell that starts with =, +, - or @ is prefixed with an apostrophe so it never runs as a formula (Q7)
- D8. Only admin and finance roles can export, the same roles that can see the report today (Q8)
- D9. The download streams immediately; the largest realistic export (one year, all campaigns) is about 40,000 rows, well within one request (Q9)

### Open assumptions
None.

### Deferred or out of scope (decided by the human)
- XLSX or PDF formats: CSV covers the need
- Scheduled or emailed exports: later
- Choosing columns: fixed column set for now

### Glossary terms touched
- **Donations report**: flagged: the glossary called it "transaction report" in one place; settled on Donations report (GLOSSARY.md)

### ADRs written
none

### Facts looked up
- Repo languages: Go backend, React + TypeScript frontend; the export is built in the Go API: repo layout
- Report query for one year across all campaigns returns about 40,000 rows in under 2 seconds: query plan on staging
- Donations can be anonymous via a flag on the donation: donation model
- Existing report tests are table tests at the HTTP handler: report handler tests

### Verification-level hint (provisional; spec makes the final call)
**Level:** B
- Q1 named states/statuses: no, the export has no lifecycle; donation status is only read
- Q2 concurrency, duplicate, late, or out-of-order events: no, a single synchronous read
- Q3 money or exactly-once effects: no, read-only; nothing is created or moved
- Q4 rule or calculation with a law for all inputs: yes, the file must round-trip the report rows and match the report total for any filter
**Reason:** a read-only transform whose correctness is a law over all inputs. Candidate invariants or properties: parsing the CSV gives back the same rows as the report; the sum of the amount column equals the report total; no cell can be read as a formula; anonymous donors never appear by name or email; row count equals the report's count.

### Next
Run `spec` with this summary.
