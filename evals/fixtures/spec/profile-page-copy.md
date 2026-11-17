<!-- vflow:decision-summary -->
## Decision summary: Profile page copy refresh

**Source:** grill session, 2026-11-14. **Tracker issue:** #163 Profile page: refresh copy. **Confirmed by:** Sari (UX writer), 2026-11-14.

### Problem and goal
Support gets questions because the profile page copy is vague ("Terjadi kesalahan") and the delete-account dialog uses "Ya / Tidak". Done when the five texts below show the approved copy in Indonesian and English and the support questions about them stop.

### Settled decisions
- D1. Only these five texts change; field labels stay as they are (Q1)
- D2. Page title: "Profil Pengguna" → "Profil Saya" (en: "My profile") (Q2)
- D3. Empty bio: "Belum ada data" → "Kamu belum menulis bio. Ceritakan sedikit tentang dirimu." with a "Tulis bio" button (en: "You haven't written a bio yet. Tell people a little about yourself." / "Write bio") (Q3)
- D4. Save toast: "Data berhasil disimpan" → "Profil tersimpan." (en: "Profile saved.") (Q4)
- D5. Save error: "Terjadi kesalahan" → "Profil belum tersimpan. Periksa koneksi internet, lalu coba lagi." (en: "Your profile wasn't saved. Check your connection and try again.") (Q5)
- D6. Delete-account dialog: title "Hapus akun?", body "Semua data profil dan riwayatmu akan dihapus permanen. Tindakan ini tidak bisa dibatalkan.", buttons "Hapus akun" / "Batal" (en: "Delete account?", "All your profile data and history will be permanently deleted. This can't be undone.", "Delete account" / "Cancel") (Q6)
- D7. The product addresses users as "kamu" on this page (Q7)
- D8. No feature flag; copy-only and easy to revert (Q8)

### Open assumptions
None.

### Deferred or out of scope (decided by the human)
- Mapping the two backend error codes that still show raw English messages: separate ticket
- Copy on other pages: later

### Glossary terms touched
none

### ADRs written
none

### Facts looked up
- All profile copy lives in the i18n files (id and en) under the profile keys; nothing is hardcoded: frontend locales
- Component tests for the profile page already exist (Vitest + Testing Library) and find text through the i18n keys: profile page tests

### Verification-level hint (provisional; spec makes the final call)
**Level:** C
- Q1 named states/statuses: no
- Q2 concurrency, duplicate, late, or out-of-order events: no
- Q3 money or exactly-once effects: no
- Q4 rule or calculation with a law for all inputs: no
**Reason:** display copy only. Candidate invariants or properties: none; example checks per text in both languages.

### Next
Run `spec` with this summary.
