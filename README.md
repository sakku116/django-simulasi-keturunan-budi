# TEST PROGRAMMER PYTHON

## how to run server
1. pastikan sudah terinstall semua package yang ada di requirements.txt. atau buat virtual environment python dan aktifkan. lalu jalankan perintah `pip install -r requirements.txt`

2. pastikan berada pada direktori base (direktori dimana readme.md berada). lalu jalankan perintah `python manage.py runserver`

## api-endpoint
- api/
    - anak-budi/ (mendapatkan semua anak budi)
    - cucu-budi/?jenis_kelamin=pria/wanita (mendapatkan semua keturunan budi (keturunan nomor 2/cucu))
    - bibi-dari/<nama> (mendapatkan bibi dari nama (keturunan dengan nomor diatas nama tersebut dan wanita))
    - bibi-dari/<nama> (mendapatkan paman dari nama (keturunan dengan nomor diatas nama tersebut dan pria))
    - sepupu-dari/<nama>?jenis_kelamin="pria/wanita" (mendapatkan semua sepupu dari nama (keturunan dengan nomor yang sama))
    - orang/ (mendapatkan informasi data tabel dari semua nama yang ada)
    - orang/<nama_or_id> (mendapatkan informasi data tabel dari nama)

## struktur db
- id (integer, autoincrement)
- nama (varchar, not null)
- jenis_kelamin (varchar, not null)
- keturunan_ke (int)
- keturunan_dari (int) # id dari orang tua

## challenge
1. Buat rancangan 1 table saja untuk menyimpan data di atas.

    dibuat dengan menggunakan database sqlite3.
2. Input data sesuai dengan silsilah di atas
    
    sudah.
3. Buat query untuk mendapatkan semua anak Budi
    hit endpoint : `api/anak-budi`
4. Buat query untuk mendapatkan cucu dari budi
    hit endpoint : `api/cucu-budi/`
5. Buat query untuk mendapatkan cucu perempuan dari budi.
    hit endpoint : `api/cucu-budi/?jenis_kelamin=wanita`
6. Buat query untuk mendapatkan bibi dari Farah
    hit endpoint : `api/bibi-dari/farah`
7. Buat query untuk mendapatkan sepupu laki-laki dari H
ani
    hit endpoint : `api/sepupu-dari/hani?jenis_kelamin=pria`
8. Rancang dan buat API yang bisa dibuat untuk kasus di atas

    dibuat menggunakan framework django. dan tidak menggunakan model.
9. Buat aplikasi CRUD sederhana untuk silsilah keluarga menggunakan Python

    pergi ke url : '/' (index).
10. Buat visualisasi tree untuk data yang diinput di nomer 1
    
    pada halaman '/' (index) sudah tertera visualisasi tree.