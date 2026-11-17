---
name: lugas
description: "Tulis, sunting, atau tulis ulang teks Bahasa Indonesia supaya lugas, inklusif, dan langsung dipahami sejak dibaca pertama kali. Write or edit plain, inclusive Indonesian. Gunakan untuk UI copy dan microcopy (tombol, pesan error, empty state, konfirmasi, onboarding), panduan, dokumentasi, laporan, pengumuman, komunikasi layanan publik, atau saat diminta 'bikin lebih lugas', 'bikin mudah dipahami', 'sederhanakan bahasanya', 'tulis ulang biar nggak kaku'. Juga untuk membalas pengguna berbahasa Indonesia dengan bahasa yang jelas dan menjelaskan istilah teknis ke orang awam. Memakai lensa RASA (Ritmis, Akurat, Sarat Makna, Alami) dan cek akhir. Bukan untuk teks berbahasa Inggris, menulis kode, menulis spec fitur (pakai spec), atau wawancara desain sebelum spec (pakai grill)."
license: "MIT. Original text; idea inspired by the bahasa-indonesia-plain gist by orepras; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: writing
---

# lugas

Skill menulis untuk Bahasa Indonesia yang polos dan jelas. Tujuannya satu: pembaca langsung mengerti pada bacaan pertama, sementara isi, ketelitian, dan nuansanya tetap utuh. Menyederhanakan bahasa tidak sama dengan menyederhanakan isi.

Skill ini berdiri sendiri. Ia bukan bagian dari alur vflow (`grill`, `spec`, dan lainnya), tapi bisa dipakai untuk merapikan bahasa di dokumen mana pun.

## Kapan dipakai

- UI copy dan microcopy: label tombol, pesan error, pesan sukses, empty state, tooltip, dialog konfirmasi, onboarding.
- Panduan, dokumentasi pengguna, README untuk orang nonteknis, laporan, pengumuman, notifikasi.
- Menulis ulang teks yang kaku, birokratis, atau terasa seperti terjemahan.
- Menjelaskan hal teknis ke orang awam, misalnya admin yayasan atau pemilik usaha kecil.

Yang tidak diubah: kode, nama fungsi, perintah terminal, path file, kutipan langsung, dan istilah hukum yang bunyinya wajib persis. Semua itu tetap ditulis apa adanya.

## Cara kerja

1. **Kenali pembacanya.** Siapa yang membaca, apa yang ingin mereka lakukan atau putuskan, dan di mana mereka membacanya (layar ponsel, email, papan pengumuman). Kalau tidak jelas, anggap pembacanya orang dewasa umum yang sibuk dan membaca di ponsel.
2. **Tulis intinya dulu dalam satu kalimat.** Kalau intinya belum bisa ditulis dalam satu kalimat, isinya yang belum jelas, bukan bahasanya. Tanyakan ke pemberi tugas.
3. **Susun dengan piramida terbalik.** Kesimpulan atau tindakan di depan, rincian di tengah, latar belakang di belakang. Pola ini berlaku untuk dokumen, bagian, paragraf, sampai kalimat.
   Untuk pengumuman dan instruksi, kalimat pertama menyebut apa yang harus dilakukan pembaca dan batas waktunya, dalam kalimat aktif yang menyapa pembaca langsung: "Mulai 5 Januari 2027, daftar ulang lewat aplikasi dan unggah foto KK paling lambat 20 Januari." Dua langkah berurutan dari satu tindakan (daftar lalu unggah) tetap satu ide dan boleh di satu kalimat.
4. **Tulis drafnya** dengan prinsip di bawah.
5. **Uji dengan RASA** dan **cek akhir**. Perbaiki, lalu serahkan.

Saat menulis ulang teks orang lain, pertahankan semua fakta, angka, tenggat, dan kewajiban. Kalau ada kalimat yang maknanya ambigu, tandai dan tanyakan. Jangan menebak.

## Prinsip inti

**Kalimat**
- Satu kalimat, satu ide. Kalau ada "dan" yang menyambung dua gagasan berbeda, pecah jadi dua kalimat.
- Panjang kalimat umumnya 12–20 kata, paling panjang 25. Selingi dengan kalimat pendek supaya tidak monoton.
- Pakai kalimat aktif: sebut siapa melakukan apa. "Tim kami mengecek pembayaranmu dalam 1 hari kerja", bukan "Pembayaran akan dilakukan pengecekan oleh tim".
- Satu paragraf, satu topik. Paragraf di layar ponsel sebaiknya 2–4 kalimat.

**Kata**
- Pilih kata yang biasa diucapkan orang, bukan gaya surat dinas: "pakai" untuk "melakukan pemanfaatan", "supaya" untuk "dalam rangka". Daftar lengkapnya ada di `references/kata.md`.
- Hindari kata benda bentukan yang menyembunyikan kata kerja: "lakukan pendaftaran" jadi "daftar", "melakukan pengecekan" jadi "cek".
- Konkret: sebut angka, tanggal, nama menu, dan batas waktu yang sebenarnya. Buang kata kabur seperti "segera", "beberapa", "dan lain-lain" kalau bisa diganti fakta.
- Istilah asing dan teknis: pakai padanan Indonesia yang umum. Kalau istilahnya memang harus dipakai, jelaskan saat pertama muncul.
- Buang kata yang tidak menambah makna. Kalimat lebih pendek biasanya lebih jelas.

**Sapaan dan nada**
- Pilih satu sapaan dan konsisten dalam satu produk. Untuk produk yang santai seperti Zekaa ("Zekaa, kelola tanpa ribet"), pakai "kamu". Untuk organisasi, pakai "kami".
- Kalau pemberi tugas menyebut sapaan, sapaan itu harus benar-benar muncul di teks, setidaknya sekali ("kamu" atau "-mu"). Kalimat santai tanpa sapaan belum menunjukkan nadanya.
- Santai bukan berarti asal. Hindari singkatan chat ("yg", "gmn") dan bahasa gaul yang cepat basi.

## Bahasa yang aman dan inklusif

Ringkasnya:
- Sebut orangnya dulu, kondisinya kemudian: "orang dengan gangguan penglihatan". Ikuti istilah yang dipilih komunitasnya sendiri, misalnya "Tuli".
- Jangan pakai kata yang menstigma, lelucon berbasis SARA atau fisik, atau anggapan tentang keluarga dan hidup yang "normal".
- Jangan menyalahkan pembaca. Jelaskan apa yang terjadi dan apa langkah berikutnya.
- Beri kendali: kabari sebelum sesuatu terjadi, terutama kalau tidak bisa dibatalkan.
- Jangan menciptakan rasa terburu-buru palsu.
- Sajikan angka supaya mudah dicerna, termasuk untuk pembaca yang kesulitan dengan angka (diskalkulia): jangan menumpuk angka, beri pembanding, tunjukkan hitungannya.
- Jangan anggap semua pembaca tinggal di kota besar, punya internet cepat, atau punya rekening bank.

Rincian dan contohnya ada di `references/inklusif.md`.

## Ejaan, angka, dan format

Ikuti EYD. Yang paling sering salah: huruf besar dipakai untuk nama diri dan awal kalimat saja (judul dan tombol cukup berhuruf besar di kata pertama), `Rp25.000` tanpa spasi, ribuan dengan titik, jam `09.30`, tanggal `17 November 2026`. Rinciannya ada di `references/ejaan-dan-format.md`.

Untuk format: pakai judul dan daftar untuk struktur, bukan cetak tebal atau huruf kapital untuk penekanan. Teks tautan harus menjelaskan tujuannya, jangan "klik di sini".

## UI copy dan microcopy

Pola untuk tombol, error, empty state, sukses, konfirmasi, form, dan notifikasi ada di `references/ui-copy.md`. Tiga aturan yang paling sering dipakai:
- Tombol memakai kata kerja yang menyebut hasilnya: "Kirim laporan", bukan "OK" atau "Submit".
- Pesan error berisi tiga hal: apa yang terjadi, tanpa menyalahkan, dan apa yang bisa dilakukan sekarang. Kalau gagalnya di tengah alur (unggah, form, pembayaran), tambahkan apa yang tetap aman: "Data lainnya tetap tersimpan."
- Konfirmasi untuk tindakan berbahaya menyebut akibatnya dengan spesifik.

## Kalimat yang terasa Indonesia

Hindari pola yang terasa hasil terjemahan dari bahasa Inggris:
- "Kamu bisa mengatur pengingat di menu Jadwal", bukan "Pengaturan pengingat dapat dilakukan melalui menu Jadwal".
- "Laporan bulan ini sudah siap", bukan "Laporan untuk bulan ini telah berhasil di-generate".
- "-lah" dan "-kah" dipakai seperlunya saja. Terlalu sering membuat teks terdengar seperti pidato.

## Konteks lokal

Kalau layananmu melayani wilayah tertentu, siapkan terjemahan atau keterangan dalam bahasa setempat, setidaknya untuk instruksi penting dan pesan darurat. Pakai contoh dan nama orang dari berbagai daerah di Indonesia.

## Lensa RASA

Setelah draf jadi, nilai dengan empat pertanyaan. Rubrik lengkapnya ada di `references/rasa.md`.

- **Ritmis:** apakah enak dibaca keras-keras, tanpa tersandung?
- **Akurat:** apakah tiap pilihan kata pas maknanya, tanpa sekadar "kira-kira"?
- **Sarat Makna:** apakah setiap baris membawa isi, tanpa bagian yang bertele-tele?
- **Alami:** apakah terdengar seperti orang sungguhan yang berbicara, tanpa kesan template atau terjemahan?

## Untuk balasan agen sehari-hari

Saat membalas pengguna berbahasa Indonesia dalam percakapan biasa, terapkan versi ringkas ini di setiap balasan, tanpa perlu menjalankan seluruh proses di atas:

1. Jawaban atau kesimpulan di kalimat pertama. Alasan dan rincian menyusul.
2. Kalimat pendek, satu ide per kalimat.
3. Jelaskan istilah teknis saat pertama muncul, dalam satu anak kalimat.
4. Jangan pakai jargon bahasa Inggris tanpa penjelasan. Kalau ada padanan Indonesia yang umum, pakai itu.
5. Sebut hal yang konkret: angka, nama file, path, perintah, tautan. Jangan cuma "beberapa file".
6. Kalau butuh keputusan dari pengguna, tulis pertanyaannya dengan jelas di akhir.
7. Kode, perintah, nama fungsi, dan teks kutipan tetap ditulis persis seperti aslinya.

Untuk dipasang di `AGENTS.md` atau `CLAUDE.md` sebuah repo, salin blok dari `references/agents-snippet.md`.

## Cek akhir

Sebelum menyerahkan, pastikan:
- [ ] Inti atau tindakan utama ada di awal.
- [ ] Orang yang baru pertama membaca paham setiap kalimat tanpa membaca ulang.
- [ ] Kalimat aktif, pendek, satu ide. Tidak ada kata yang bisa dibuang tanpa mengubah makna.
- [ ] Semua fakta, angka, dan tenggat dari teks asal masih ada dan benar.
- [ ] Tidak ada jargon tanpa penjelasan, tidak ada penekanan dengan huruf kapital. Ini termasuk istilah yang dipakai pemberi tugas sendiri (misalnya "cloud" atau "server" dalam permintaan): pembaca akhirnya belum tentu tahu artinya.
- [ ] Aman dibaca orang yang sedang panik, sedih, atau kesulitan dengan angka.
- [ ] Bebas stigma dan anggapan tentang "normal".
- [ ] Lulus keempat pertanyaan RASA.

Saat menyerahkan hasil tulis ulang, sertakan catatan singkat soal perubahan utamanya dan hal yang perlu dikonfirmasi oleh pemberi tugas.
