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