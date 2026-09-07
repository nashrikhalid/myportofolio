Nama : Nashri Khalid

NPM : 2506657131

Kelas : PBP F

### Tugas 1
1. Saya pakai beberapa elemen semantik seperti header, nav, main, section, dan footer untuk membagi halaman jadi bagian bagian yang jelas, hero, skills, projects, dan experiences masing masing jadi section sendiri. Ini membantu karena CSS jadi lebih mudah di-scope per bagian dan strukturnya lebih rapi dibanding tumpukan div. Tapi saya belum pakai article atau aside, padahal  bagian project dan pengalaman organisasi cocok pakai article karena berisi konten yang berdiri sendiri, mungkin ini salah satu hal yang masih bisa diperbaiki.

2. Tantangan paling terasa ada di bagian hero yang pakai grid dua kolom untuk nama dan foto. Di layar kecil itu harus disusun ulang total jadi satu kolom, jadi saya definisikan ulang tata letaknya khusus untuk mobile. Ukuran foto juga sempat jadi masalah karena awalnya pakai persentase yang pas di desktop tapi kebesaran di mobile, jadi saya kasih batas ukuran maksimal. Untuk menentukan prioritas, saya utamakan elemen yang paling penting buat identitas seperti nama dan foto supaya tetap jelas duluan, sementara elemen pelengkap seperti ikon sosial media dibiarkan menyesuaikan kalau memang ruangnya gak cukup.

3. Karena masih static murni, isi seperti daftar project itu saya tulis langsung di HTML, jadi kalau mau nambah atau ubah project harus edit kode dan deploy ulang, gak bisa diubah dari luar. Form kontak juga masih sekadar mailto biasa, belum benar benar terkirim ke sistem manapun. Untuk iterasi berikutnya saya pengen bagian project dan pengalaman itu jadi dinamis, diambil dari database lewat Django, supaya saya bisa menambah atau ubah isi tanpa harus rekonstruksi HTML setiap kali, dan kalau memungkinkan bikin form kontak yang beneran menyimpan atau mengirim pesan.

Link AI Gemini: https://share.gemini.google/8Z5QrcVPK2Ot
Figma (unserious prototype): https://www.figma.com/proto/IZiorW1v0Emom9gu1nJZGP/myporto--?node-id=1-2&t=9DPZXGBu5VvgDBmr-1