# Tutorial 07: DRF

API baru tersedia di /api/v1/projects/ dan /api/v1/experiences/.
Tambahkan UUID dan slash untuk detail; tambahkan star/ untuk toggle star.
GET membaca, POST membuat, PUT mengganti field wajib, PATCH mengubah sebagian,
DELETE menghapus (204 tanpa body). POST pada star/ memakai pengguna session.

Serializer menerjemahkan model dan memvalidasi input. Permission memeriksa peran.
SessionAuthentication memakai login Django; operasi tulis membutuhkan CSRF.
Projects hanya dikelola superuser. Experiences juga dapat diubah Editor,
tetapi pembuatan dan penghapusan tetap hanya untuk superuser.

Kedua halaman memakai JSON datar, AJAX tambah/hapus/star, pencarian debounce,
AbortController, toast, dan escaping. Form edit lama tetap tersedia.
Tidak ada perubahan model atau database. Endpoint lama dipertahankan.

Jalankan:
```
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py test main
```

Sesudah pemeriksaan lokal, deploy melalui alur PWS yang sudah digunakan,
periksa login dan operasi tulis di HTTPS, lalu kumpulkan tautan commit GitHub
ke SCELE. Jangan sertakan .env, database, atau environment.
