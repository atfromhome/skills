# Uji skill dengan Claude Code CLI (`vtest.py`)

`vtest.py` menguji skill di repo ini dengan Claude Code sungguhan. Claude Code menjawab tiap kasus di `evals/`. Lalu Claude Code dipanggil lagi di sesi terpisah sebagai penilai.

## Syarat
- Claude Code sudah terpasang dan login (`claude --version`).
- Python 3 dan git.

## Langkah (dari root repo)

```bash
python3 evals/vtest.py setup                 # buat sandbox, pasang semua skill
python3 evals/vtest.py triggers grill        # uji pemicu
python3 evals/vtest.py behavior grill        # uji perilaku + penilaian otomatis
python3 evals/vtest.py report                # rekap ke evals/.vtest/results/REKAP.md
```

Tanpa nama skill, semua skill diuji. Hasil disimpan di `evals/.vtest/` (diabaikan git).

## Opsi
- `--only 1,3`: hanya kasus nomor 1 dan 3.
- `--model sonnet` atau `--model opus`: pilih model.
- `--turns N`: jumlah giliran percakapan. Default 5 untuk grill dan chart, 3 untuk spec dan ship, 2 untuk slice dan check, 1 untuk lainnya. User simulasi menyetujui semua rekomendasi.
- `--max-turns 12`: batas langkah per giliran.

## Hasil
- `results/REKAP.md`: ringkasan, yang gagal, dan saran perbaikan SKILL.md.
- `results/answers/<skill>-<no>.md`: jawaban lengkap. Baca ini sebelum mengubah skill.

## Catatan
- Claude hanya boleh memakai Skill, Read, Glob, dan Grep. Langkah yang butuh repo atau GitHub ditulis sebagai [SIMULASI].
- Skill pribadi di `~/.claude/skills` tetap aktif dan bisa bentrok. `setup` memberi tahu kalau ada.
- Tiap kasus perilaku butuh beberapa panggilan Claude. Mulai dari satu skill.
- Penilai bisa keliru. Cek `answers/` untuk kasus yang gagal.

## Menjalankan lewat Claude Code
Buka `claude` di root repo, lalu minta: "Jalankan evals/vtest.py untuk grill, spec, dan lugas sesuai evals/VTEST.md. Baca REKAP.md dan answers/, tentukan tiap kegagalan karena skill atau cara uji, lalu usulkan perubahan SKILL.md tanpa mengubah file."
