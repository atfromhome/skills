# multica

Script untuk membangun ulang setup Multica kita di workspace lain. Setup-nya: workflow **Delivery**, Implementator Squad, enam agen (Imad, Comapp, Lemen, Revie, Refiner, Qeea), skill vflow, dan status board.

Isinya tiga file:

| File | Gunanya |
|---|---|
| `delivery.json` | Config setup. Tidak ada ID workspace di dalamnya, jadi bisa dipakai di workspace mana pun. Agen, squad, dan status dirujuk lewat nama atau key. |
| `rebuild.py` | Membaca `delivery.json`, lalu membuat yang belum ada di workspace tujuan. |
| `export.py` | Membuat ulang `delivery.json` dari workspace sumber. Hanya membaca, tidak mengubah apa pun. |

## Yang perlu disiapkan

- Python 3. Tidak perlu paket tambahan.
- CLI `multica` (versi 0.10.0 sudah dicoba) dan sudah login. Cek dengan `multica workspace list`.
- Peranmu di workspace tujuan owner atau admin. Workflow hanya bisa diatur oleh peran ini.
- Daemon Multica menyala dan punya runtime Claude yang online. Agen baru dipasang ke runtime ini.

## Cara pakai

Selalu mulai dengan `--dry-run`. Script hanya membaca workspace dan menampilkan perintah yang akan dijalankan.

```bash
python3 multica/rebuild.py --workspace-id drm --status-map qa=quality_assurance --dry-run
```

Kalau hasilnya sudah sesuai, jalankan tanpa `--dry-run`:

```bash
python3 multica/rebuild.py --workspace-id drm --status-map qa=quality_assurance
```

`--workspace-id` bisa diisi ID lengkap, slug, atau nama yang persis. Contoh `drm` jalan kalau slug workspace-nya memang `drm`.

`workspace list` di CLI 0.10.0 hanya mengembalikan id, nama, dan slug. Issue prefix tidak ada di situ. Kata `prefix` pada `workspace member list` adalah awalan UUID, paling pendek 4 karakter hex. Kalau tidak ketemu, script menampilkan daftar workspace yang ada. Pakai ID lengkap kalau ragu.

Pilihan lain:

| Flag | Gunanya |
|---|---|
| `--status-map qa=quality_assurance` | Pakai status yang sudah ada, bukan membuat yang baru. Di contoh ini, status QA di config memakai status Quality Assurance di workspace tujuan. Bisa diulang. |
| `--runtime-id <id>` | Pilih runtime untuk agen baru. Kalau kosong, script memakai runtime Claude pertama yang online dan menyebut pilihannya. |
| `--member-id <user-id>` | Orang yang memegang langkah Ready dan In Review. Kalau kosong, script memakai owner workspace. |
| `--config <file>` | Pakai config lain. Default-nya `multica/delivery.json`. |
| `--raw-category` | Kirim kategori status apa adanya. Lihat bagian Batasan. |

## Urutan kerja script

1. Impor skill dari `github.com/atfromhome/skills`.
2. Buat status yang belum ada. Di "Dari Rumah Pertama", ini berarti status Ready.
3. Buat agen, lengkap dengan model, deskripsi, dan instruksinya.
4. Pasang skill ke tiap agen.
5. Buat Implementator Squad, isi instruksinya, lalu tambahkan anggotanya.
6. Buat workflow Delivery. Kalau workflow dengan nama itu sudah ada, langkahnya diperbarui.

Script aman dijalankan berkali-kali. Yang sudah ada dipakai lagi, tidak dibuat dobel. Kalau ada perintah yang gagal, perbaiki penyebabnya lalu jalankan ulang. Langkah yang sudah jadi akan dilewati.

Di akhir, script mencetak ringkasan: apa yang dibuat, apa yang dipakai ulang, dan ID-nya.

## Memperbarui config

Kalau setup di workspace sumber berubah, buat ulang `delivery.json`:

```bash
python3 multica/export.py --workspace-id <id-workspace-sumber> --workflow Delivery --out multica/delivery.json
```

`export.py` tidak menyimpan `custom_env`, `mcp_config`, atau ID runtime. Nilai-nilai itu sering berisi rahasia atau hanya berlaku di satu mesin. Key status yang diberi akhiran angka, misalnya `ready_2`, ditulis ulang jadi `ready`.

## Batasan

- Script ini belum pernah dijalankan ke API Multica yang asli. Pengujiannya memakai CLI tiruan yang mengembalikan data ekspor. Jadi jalankan `--dry-run` dulu dan baca perintahnya.
- Bantuan `multica issue-status create` menyebut kategori `backlog, unstarted, started, done, closed`. Data ekspor memakai `todo` dan `in_progress`. Script memetakan `todo` ke `unstarted` dan `in_progress` ke `started`. Kalau CLI menolak, ulangi dengan `--raw-category`.
- Perintah `workflow create` tidak ada di cuplikan bantuan CLI yang dicek. Di kode CLI 0.10.0 flag-nya `--name`, `--description`, dan `--steps-file`, sama dengan yang script kirim. Belum dicoba ke API.
- Agen yang sudah ada tidak diubah. Kalau instruksinya beda, ubah lewat UI.
- Avatar agen belum ikut dibuat karena `agent create` tidak punya flag untuk avatar.
- Workflow baru belum dipasang ke project mana pun. Pasang lewat Settings → Workflows.
