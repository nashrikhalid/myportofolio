Nama : Nashri Khalid

NPM : 2506657131

Kelas : PBP F

### Tugas 1
1. Saya pakai beberapa elemen semantik seperti header, nav, main, section, dan footer untuk membagi halaman jadi bagian bagian yang jelas, hero, skills, projects, dan experiences masing masing jadi section sendiri. Ini membantu karena CSS jadi lebih mudah di-scope per bagian dan strukturnya lebih rapi dibanding tumpukan div. Tapi saya belum pakai article atau aside, padahal  bagian project dan pengalaman organisasi cocok pakai article karena berisi konten yang berdiri sendiri, mungkin ini salah satu hal yang masih bisa diperbaiki.

2. Tantangan paling terasa ada di bagian hero yang pakai grid dua kolom untuk nama dan foto. Di layar kecil itu harus disusun ulang total jadi satu kolom, jadi saya definisikan ulang tata letaknya khusus untuk mobile. Ukuran foto juga sempat jadi masalah karena awalnya pakai persentase yang pas di desktop tapi kebesaran di mobile, jadi saya kasih batas ukuran maksimal. Untuk menentukan prioritas, saya utamakan elemen yang paling penting buat identitas seperti nama dan foto supaya tetap jelas duluan, sementara elemen pelengkap seperti ikon sosial media dibiarkan menyesuaikan kalau memang ruangnya gak cukup.

3. Karena masih static murni, isi seperti daftar project itu saya tulis langsung di HTML, jadi kalau mau nambah atau ubah project harus edit kode dan deploy ulang, gak bisa diubah dari luar. Form kontak juga masih sekadar mailto biasa, belum benar benar terkirim ke sistem manapun. Untuk iterasi berikutnya saya pengen bagian project dan pengalaman itu jadi dinamis, diambil dari database lewat Django, supaya saya bisa menambah atau ubah isi tanpa harus rekonstruksi HTML setiap kali, dan kalau memungkinkan bikin form kontak yang beneran menyimpan atau mengirim pesan.

Link AI Gemini: https://share.gemini.google/8Z5QrcVPK2Ot
Figma (unserious prototype): https://www.figma.com/proto/IZiorW1v0Emom9gu1nJZGP/myporto--?node-id=1-2&t=9DPZXGBu5VvgDBmr-1


### Tugas 2
1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.
Saat pengguna enter link portofolio ke browser, browser mengirimkan permintaan http ke server webservice (pws.cs.ui.ac.id untuk portofolio ini). Lalu urls.py proyek menangkap permintaan tersebut dan mengarahkan ke urls.py aplikasi untuk menampilkan landing page dan view-view selanjutnya yang diinginkan user. Saat pengguna ingin melihat bagian lain seperti experiences atau projects, url.py mengarahkan ke view experiences atau projects. View akan menghubungi model sesuai yang dihubungkan dengan view tersebut (ditandai melalui syntax Experience.objects.all). Setelah view mengumpulkan seluruh data di context, fungsi di view akan render template html yang akan ditampilkan untuk merepresentasikan datanya.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.
Jika ditulis langsung di dalam template (hardcode), akan menyulitkan proses pengembangan di kemudian hari karena kode harus diketik manual dan bisa saja berpengaruh buruk pada kode lain yang sudah baik sebelumnya, yang menyebabkan kode harus disesuaikan lagi. Pemeliharaan juga akan menjadi lebih sulit karena kode akan menjadi sangat banyak (spaghetti code). Dengan disimpan pada model, data portofolio yang akan ditambah hanya perlu diisi melalui shell/django admin dan akan ditambah otomatis sesuai ketentuan di model, view, dan html. 

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.
makemigrations berfungsi untuk mencatat perubahan pada model dan membuat blueprint perubahan yang dimasukkan ke folder migrations. Selanjutnya untuk mengeksekusi perubahan model, perlu diketikkan migrate sehingga blueprint akan dieksekusi ke database db.sqlite3. Contoh perubahan model yang mengharuskan dijalankan kedua instruksi tersebut adakah saat menambah, menghapus, atau mengubah struktur field/kolom data di dalam model

Link AI Gemini: https://share.gemini.google/4GiuYLARFaRh


### Tugas 3
1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
...

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
...

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
...

Link AI Gemini: 