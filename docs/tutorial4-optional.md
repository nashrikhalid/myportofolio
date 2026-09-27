# Tutorial 4 opsional: Selenium dan Burp Suite

## Persiapan

Aktifkan virtual environment, lalu jalankan:

```powershell
python -m pip install -r requirements-dev.txt
```

Isi `E2E_USER_PASSWORD` dan `E2E_ADMIN_PASSWORD` dalam `.env` dengan password uji. Jangan commit `.env`, nilai cookie, atau request login mentah. Kredensial E2E lokal telah disiapkan tanpa dicetak ke log.

## Selenium

```powershell
python test_e2e.py --headless
# Untuk melihat browser:
python test_e2e.py
```

Skrip otomatis menjalankan server di `127.0.0.1` pada port sementara dan database uji terpisah. Tidak perlu `runserver` terpisah. Akun `visitor_e2e` dan `owner_e2e` hanya dibuat pada database uji; akun asli tidak diubah. Database uji dan Chrome ditutup setelah tes selesai. Mode produksi/non-SQLite ditolak.

Pemeriksaan:

1. Form login mempunyai hidden input CSRF dan cookie `csrftoken`.
2. Login menerbitkan `sessionid` dan `last_login`; username tampil pada navbar.
3. Session mengenali pengguna saat pindah halaman.
4. Akun biasa ditolak dari tambah proyek; superuser dapat membuka form.
5. POST tanpa token CSRF ditolak dan tidak membuat proyek.
6. Logout menghapus kedua cookie login.

Screenshot tersimpan di `artifacts/tutorial4/` yang diabaikan Git. Tes tanpa `--burp` menghapus token melalui DOM Selenium; ini bukan bukti intersepsi Burp.

## Burp: intersepsi nyata

Burp resmi tersimpan lokal di `.local-tools/burpsuite.jar` (diabaikan Git). Jalankan dengan Java:

```powershell
java -jar .local-tools/burpsuite.jar
```

Pilih Community Edition, temporary project, dan konfigurasi default. Proxy lokal memakai `127.0.0.1:8080`. Mulai dengan **Intercept off**.

```powershell
python test_e2e.py --burp
```

Mode ini memakai Chrome Selenium dengan proxy Burp, sehingga tidak perlu mengubah proxy Windows. Seluruh akun dan proyek tetap berada pada database uji sementara.

1. Tunggu terminal menampilkan `[BURP READY]`. Browser sudah login sebagai superuser dan form proyek sudah terisi.
2. Di Burp buka **Proxy > Intercept**, aktifkan **Intercept on**.
3. Kembali ke terminal dan tekan Enter. Skrip mengirim form.
4. Di Burp pilih request **POST /projects/add/** menuju `127.0.0.1`. Jika request lain tertahan, teruskan tanpa perubahan hingga request tersebut muncul.
5. Di body request, kosongkan nilai `csrfmiddlewaretoken` (atau hapus parameternya). Biarkan cookie session dan field lain tetap ada. Klik **Forward**.
6. Browser harus menerima **403 Forbidden / CSRF verification failed**. Skrip memeriksa bahwa proyek tidak tersimpan dan menyimpan screenshot `03-burp-csrf.png`.
7. Matikan **Intercept**, lalu tekan Enter di terminal untuk menyelesaikan logout dan cleanup.

Jika eksperimen melebihi enam menit, skrip gagal dan membersihkan browser/database; ulangi dengan Intercept off. Jangan mengaktifkan proxy terhadap server PWS atau website lain untuk eksperimen ini.

Perbedaan dua 403: akun biasa ditolak karena otorisasi; superuser dengan token hilang ditolak oleh middleware CSRF sebelum view dijalankan. Cookie session yang sah tidak menggantikan token CSRF.

## Hasil pelaksanaan, 28 September 2026

- Selenium/Chrome: alur login, cookie, session lintas halaman, penolakan akun biasa, akses superuser, CSRF, dan logout berhasil.
- Burp Community 2026.7.3: POST lokal `/projects/add/` benar-benar ditahan di Proxy > Intercept. Nilai `csrfmiddlewaretoken` dikosongkan melalui Inspector lalu **Apply changes > Forward**. Browser menerima 403 dengan teks `CSRF verification failed. Request aborted.`; tes selesai `OK` dan Intercept dimatikan kembali.
- Pengujian regresi Django: 12 tes lolos.
- Eksperimen memakai Chrome Selenium melalui Burp, bukan browser bawaan Burp. Server dan database dibuat sementara oleh skrip; PWS dan database akun asli tidak digunakan.
- Bukti respons browser: `artifacts/tutorial4/03-burp-csrf.png`. Screenshot dan binary lokal tidak masuk commit.

## Referensi resmi

- [Selenium Python](https://www.selenium.dev/selenium/docs/api/py/)
- [Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/)
- [Intersepsi HTTP dengan Burp Proxy](https://portswigger.net/burp/documentation/desktop/getting-started/intercepting-http-traffic)
- [Unduhan resmi Burp 2026.7.3 dan checksum](https://portswigger.net/burp/releases/professional-community-2026-7-3)
