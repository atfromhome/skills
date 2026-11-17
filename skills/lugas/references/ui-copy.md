# Pola UI copy dan microcopy

Contoh memakai nada santai dengan sapaan "kamu", seperti produk Zekaa ("Zekaa, kelola tanpa ribet"). Sesuaikan sapaan dengan produkmu.

## Tombol dan tautan aksi

- Kata kerja + objek yang menyebut hasilnya: "Simpan jadwal", "Kirim bukti transfer", "Tambah donatur".
- Hindari tombol generik: "OK", "Submit", "Proses", "Ya". Pada dialog, label tombol harus tetap masuk akal dibaca tanpa judul dialognya.
- Tombol kedua menyebut pilihannya juga: "Batal" atau "Kembali ke daftar", bukan "Tidak".

## Pesan error

Tiga bagian: apa yang terjadi, tanpa menyalahkan, apa yang bisa dilakukan sekarang.

| Kurang baik | Lebih baik |
|---|---|
| Error 500. Terjadi kesalahan. | Laporan belum bisa dibuat karena server sedang sibuk. Coba lagi dalam beberapa menit. Datamu aman. |
| Input tidak valid. | Nomor WhatsApp perlu diawali 08 atau +62, misalnya 0812 3456 7890. |
| Anda gagal login. | Email atau kata sandi belum cocok. Cek lagi, atau atur ulang kata sandi. |
| File ditolak. | File terlalu besar (12 MB). Batasnya 5 MB. Coba kecilkan fotonya dulu. |

Tampilkan pesan error di dekat kolom yang bermasalah, bukan hanya di atas halaman.

## Empty state

Jelaskan kenapa kosong dan apa langkah pertamanya.
- "Belum ada transaksi bulan ini. Catat pemasukan atau pengeluaran pertama, nanti ringkasannya muncul di sini."
- Hasil pencarian kosong: "Tidak ada donatur bernama 'Yohanes'. Cek ejaannya, atau tambahkan sebagai donatur baru."

## Pesan sukses

Singkat, konkret, sebut apa yang berubah dan langkah berikutnya kalau ada.
- "Kuitansi terkirim ke email Bu Siti."
- "Jadwal piket tersimpan. Pengingat dikirim tiap Senin pukul 07.00."

## Konfirmasi tindakan berbahaya

Sebut objeknya dan akibatnya. Tombol konfirmasi mengulang aksinya.
- Judul: "Hapus data donatur Teuku Rahmat?"
- Isi: "Riwayat 14 donasinya juga ikut terhapus dan tidak bisa dikembalikan."
- Tombol: "Hapus permanen" dan "Batal".

Kalau tindakan bisa dibatalkan, lebih baik sediakan tombol "Urungkan" setelahnya daripada dialog konfirmasi.

## Form

- Label selalu terlihat di atas kolom. Jangan menjadikan placeholder sebagai label, karena hilang saat pengguna mulai mengetik.
- Placeholder cukup berisi contoh isian: "contoh: 17 Agustus 2026".
- Tandai kolom yang opsional, bukan yang wajib, kalau sebagian besar kolom wajib.
- Teks bantuan menjawab "kenapa diminta?" atau "diisi apa?": "Kami pakai untuk mengirim kuitansi, bukan untuk promosi."

## Tooltip dan teks bantuan

Satu kalimat. Jangan menaruh informasi penting hanya di tooltip, karena sulit dibuka di ponsel.

## Onboarding

Mengajak, bukan memerintah. Tunjukkan manfaatnya.
- "Tambahkan rekening yayasan dulu, supaya donasi yang masuk langsung tercatat."
- Sediakan "Nanti saja" untuk langkah yang tidak wajib.

## Notifikasi dan pengingat

- Siapa atau apa, lalu tindakannya: "Iuran Pak Made untuk November belum tercatat. Tandai lunas?"
- Jangan menakut-nakuti atau memakai banyak tanda seru.
- Sebut tanggal dan jam yang jelas, termasuk zona waktu kalau perlu.

## Status dan proses

- Sebut yang sedang terjadi: "Sedang mengunggah 3 dari 10 foto", bukan "Loading...".
- Kalau lama, beri perkiraan waktu dan izinkan pengguna meninggalkan halaman kalau memang aman.
