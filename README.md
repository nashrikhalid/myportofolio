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
Kita pakai ModelForm karena Django sudah tahu struktur data kita dari model. Tipe input, label, batas panjang, dan status wajib-diisi diturunkan otomatis dari field model, jadi kita tidak perlu menulis definisi yang sama berulang kali di HTML, di validasi, dan di model. Kalau model berubah (misalnya nambah field), form cukup disesuaikan sedikit. Dengan form HTML manual, setiap <input> harus ditulis satu per satu dan validasinya harus dibuat sendiri di view. ModelForm juga memberi validasi di sisi server lewat form.is_valid(): cek tipe data, max_length, format URL, field wajib, lengkap dengan pesan error yang bisa ditampilkan lewat field.errors. Ini penting karena validasi di browser (atribut HTML) gampang dilewati, misalnya lewat Postman. Terakhir, form.save() langsung menyimpan data ke database, dan form yang sama bisa dipakai lagi untuk update dengan instance=, jadi create dan edit tidak butuh dua form terpisah. Untuk {% csrf_token %}: CSRF (Cross-Site Request Forgery) adalah serangan ketika situs lain memancing browser pengguna mengirim request ke situs kita tanpa sepengetahuan pengguna. Browser otomatis menyertakan cookie, jadi server bisa mengira request itu sah. Django menangkalnya dengan token unik dan rahasia yang dibuat server, lalu disisipkan ke form sebagai hidden input. Saat form di-POST, Django mencocokkan token itu, dan kalau hilang atau salah, request ditolak (403). Situs penyerang tidak bisa membaca token kita karena dibatasi same-origin policy, jadi tidak bisa memalsukannya. Itu sebabnya semua form POST, termasuk tombol hapus, wajib membawa token ini. CSRF_TRUSTED_ORIGINS di settings.py melengkapinya dengan mendaftarkan domain deployment (PWS) yang dipercaya.

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
Alasan utamanya JSON lebih ringkas. XML mewajibkan tag pembuka dan penutup untuk setiap elemen, sedangkan JSON cukup pasangan key-value, jadi ukuran datanya lebih kecil dan lebih hemat bandwidth. Parsing juga lebih cepat dan sederhana. JSON juga langsung cocok dengan struktur data di kebanyakan bahasa pemrograman. Object jadi dictionary, array jadi list, dan tipe angka, boolean, serta null sudah tersedia. Di frontend, JSON praktis "native" karena bisa langsung dipakai dengan JSON.parse() atau response.json() di JavaScript. XML butuh parser khusus dan pemrosesan tambahan (DOM), serta ada kerancuan kapan sesuatu ditulis sebagai atribut atau sebagai elemen anak. XML tetap punya kelebihan, seperti schema (XSD) dan namespace, dan masih dipakai di sistem enterprise lama, tapi untuk aplikasi web modern JSON lebih praktis.

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
Misalnya, untuk get_projects_json:
- Client (browser, Postman, atau kode lain) mengirim GET request ke URL tersebut.
- Django mencocokkan URL itu di urls.py dan memanggil view get_projects_json.
- View mengambil data dari database lewat ORM (Project.objects.all()), dan kalau ada query ?title=..., datanya     difilter dengan filter(title__icontains=...).
- Hasilnya berupa QuerySet, lalu diubah jadi string JSON dengan serializers.serialize("json", projects).
- String itu dikirim balik lewat HttpResponse(..., content_type="application/json"). Header content_type memberi tahu client bahwa isinya JSON, sehingga bisa langsung di-parse.
Di tutorial 3, show_projects juga memanggil get_projects_json, lalu hasilnya di-deserialize lagi jadi objek Python dan dikirim ke template. Kelihatannya berputar-putar, tapi ini meniru skenario nyata saat client dan server terpisah. Serialization diperlukan karena QuerySet dan objek model itu objek Python yang hidup di memori server, sedangkan HTTP hanya mengirim teks/byte. Data harus diubah dulu ke format standar yang tidak bergantung pada bahasa, supaya client mana pun (JavaScript, aplikasi mobile, dll.) bisa membacanya. Serializer Django juga menangani tipe data yang tidak bisa langsung dijadikan JSON oleh json.dumps biasa, seperti UUIDField atau tanggal, dan membungkus setiap data dengan struktur model, pk, dan fields.

Link AI Gemini: https://share.gemini.google/TEAkHw9YbMLZ


## Tugas 4
AI Disclosure: Dalam mengerjakan tugas 4, saya memakai AI untuk memahami alur autentikasi dan cookie, serta meminta penjelasan lebih rinci mengenai tutorial 4 dan contoh penerapannya di tugas 4.

## Tutorial 4 Opsional

Skrip pengujian browser dan eksperimen intersepsi CSRF tersedia dalam [panduan Selenium dan Burp Suite](docs/tutorial4-optional.md). Jalankan dengan virtual environment aktif: python test_e2e.py --headless atau python test_e2e.py --burp.

### Tugas 5

1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

   Jawab: Debouncing adalah teknik menunda pemanggilan fungsi sampai tidak ada event baru selama jeda waktu tertentu. Pada pencarian, timer diulang setiap kali pengguna mengetik, sehingga permintaan AJAX baru dikirim setelah pengguna berhenti mengetik selama jeda tersebut, misalnya 300 milidetik. Teknik ini mengurangi jumlah permintaan ke server, menghemat penggunaan jaringan, dan menghindari pembaruan hasil untuk setiap karakter yang diketik. Pada halaman Experiences saya, debouncing diterapkan dengan clearTimeout dan setTimeout.

2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?

   Jawab: await menunda kelanjutan fungsi async sampai Promise yang ditunggu selesai. Pada await fetch(url), kode menunggu respons sebelum memakai objek Response. Setelah itu, await response.json() menunggu pembacaan dan pengubahan isi respons JSON menjadi data JavaScript. Penantian ini tidak menghentikan seluruh browser. Tanpa await, fetch() mengembalikan Promise, sehingga kode berikutnya bisa berjalan sebelum respons tersedia. Jika Promise tersebut langsung diperlakukan sebagai Response, misalnya dengan memanggil .json(), akan terjadi error. Alternatifnya, hasil dapat ditangani dengan .then(). Dalam skrip biasa seperti pada proyek ini, await digunakan di dalam fungsi async; JavaScript juga mendukung await pada tingkat teratas sebuah modul.

   Promise adalah objek yang merepresentasikan hasil atau kegagalan suatu operasi asinkron yang mungkin belum selesai.

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

   Jawab: Cross-Site Scripting (XSS) adalah serangan ketika penyerang menyisipkan kode berbahaya ke halaman web sehingga dijalankan oleh browser pengguna lain dalam konteks situs tersebut. Contohnya adalah memasukkan tag gambar dengan atribut onerror berisi JavaScript ke kolom judul. Jika input itu dimasukkan langsung ke innerHTML, browser dapat menafsirkannya sebagai HTML dan menjalankan kode tersebut.
   Template Django secara default melakukan auto-escaping terhadap variabel yang ditampilkan, sehingga karakter khusus seperti < dan > ditampilkan sebagai teks. Ketika data JSON dirakit menjadi HTML oleh JavaScript, perlindungan template Django itu tidak otomatis berlaku pada data tersebut. Karena itu, memasukkan data mentah ke innerHTML dapat membuka celah XSS. AJAX sendiri tidak otomatis tidak aman; risikonya bergantung pada cara data ditampilkan.
   Pada proyek saya, teks dari JSON di-escape menggunakan escapeHtml sebelum disisipkan ke HTML. Alternatifnya adalah memakai textContent agar input diperlakukan sebagai teks. Input teks juga perlu dibersihkan di server menggunakan strip_tags dalam method clean_<field> pada ModelForm. Pembersihan input ini merupakan lapisan tambahan dan tidak menggantikan escaping saat menampilkan data.


#### Implementasi Tugas 5

Halaman `/experiences/` memuat data JSON beserta informasi star melalui Fetch API, menyediakan pencarian dengan debounce 300 ms, dan menampilkan kondisi loading, kosong, serta error. Superuser dapat menambahkan pengalaman melalui modal tanpa reload, dengan toast sukses atau pesan validasi. Endpoint memeriksa hak akses dan CSRF, sedangkan ExperienceForm membersihkan judul, organisasi, dan deskripsi. Teks JSON di-escape saat kartu ditampilkan. Editor tetap dapat mengedit, dan pengunjung dapat membaca daftar.

#### Menjalankan proyek secara lokal (Windows PowerShell)

Jalankan perintah berikut dari folder proyek. Jika folder `env` sudah tersedia, langkah pembuatan virtual environment dapat dilewati.

```powershell
python -m venv env
.\env\Scripts\python.exe -m pip install -r requirements.txt
$env:PRODUCTION = "False"
.\env\Scripts\python.exe manage.py migrate
.\env\Scripts\python.exe manage.py createsuperuser
.\env\Scripts\python.exe manage.py runserver
```

Pembuatan superuser cukup sekali; gunakan akun yang sudah ada jika tersedia. Mode lokal memakai SQLite dan tidak membutuhkan konfigurasi PostgreSQL produksi. Buka `http://127.0.0.1:8000/experiences/`, lalu login melalui `/login/` untuk menguji peran superuser. Untuk menguji Editor, buat grup bernama `Editor` melalui Django admin dan masukkan akun penguji ke grup tersebut. Akun biasa dapat dibuat melalui `/register/`.

Uji pencarian, hasil kosong, tambah data valid, input tidak valid, notifikasi, dan akses tanpa login. Pemeriksaan konfigurasi dapat dijalankan dengan `python manage.py check` jika virtual environment sudah aktif. Tes lama di `main/tests.py` masih memiliki ekspektasi HTML/JSON sebelum AJAX; hasilnya belum seluruhnya lulus dan perlu disesuaikan dengan alur baru.

#### AI Disclosure Tugas 5

Saya menggunakan OpenAI Codex melalui percakapan untuk memahami instruksi Tugas 5 dan menghubungkannya dengan Tutorial 5. Strategi prompting dilakukan bertahap: meminta penjelasan intuitif tentang AJAX, XSS, debouncing, dan serialization; menanyakan penyesuaian potongan kode Projects menjadi Experiences; meminta penjelasan skrip per bagian; kemudian meminta audit terhadap checklist tugas.

Codex membantu menulis skrip AJAX Experiences dan menyesuaikan field endpoint JSON, mempertahankan desain kartu, membetulkan penamaan tunggal/jamak beserta referensinya, serta memeriksa hak akses dan validasi. Codex juga membantu memperbaiki pembersihan field organisasi, menghapus fungsi escapeHtml yang duplikat, dan merapikan jawaban reflektif serta dokumentasi ini. Jadi bantuan AI mencakup penjelasan, penulisan/perubahan kode, pemeriksaan, dan penyusunan dokumentasi.

Proses ini menunjukkan bahwa contoh kode tidak dapat langsung disalin tanpa disesuaikan: field Projects berbeda dari Experience, nama class CSS harus cocok dengan desain, dan method clean_<field> harus sesuai nama field serta berada di dalam kelas form, bukan Meta. Pemeriksaan kode dan endpoint oleh AI juga belum membuktikan seluruh interaksi browser berjalan benar. Pengujian manual antarmuka dan pemeriksaan hasil akhir tetap diperlukan. Ringkasan ini merupakan catatan penggunaan AI, bukan transkrip lengkap percakapan.
