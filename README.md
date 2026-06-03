# 🐟 AquaLens — Klasifikasi Jenis Ikan Konsumsi

**AquaLens** adalah aplikasi web berbasis Flask yang mengklasifikasikan 8 spesies ikan konsumsi pasar tradisional menggunakan algoritma **Random Forest** dengan ekstraksi fitur warna (RGB + HSV). Model dilatih dari dataset Fish-gres (ITS Surabaya, Mendeley Data, DOI: 10.17632/76cr3wfhff.1).

---

## 📋 Daftar Isi

- [Demo](#demo)
- [Fitur Aplikasi](#fitur-aplikasi)
- [Spesies Ikan yang Didukung](#spesies-ikan-yang-didukung)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Instalasi & Menjalankan Lokal](#instalasi--menjalankan-lokal)
- [Melatih Ulang Model](#melatih-ulang-model)
- [Struktur Folder](#struktur-folder)
- [Deployment ke Railway](#deployment-ke-railway)
- [Konfigurasi Domain my.id (IDCloudHost)](#konfigurasi-domain-myid-idcloudhost)
- [FAQ](#faq)

---

## 🌐 Demo

> Setelah deployment, isi bagian ini dengan URL Railway atau domain kamu.

```
https://your-app.railway.app
https://aqualens.my.id   ← setelah domain dikonfigurasi
```

---

## ✨ Fitur Aplikasi

- **Klasifikasi real-time** — upload foto ikan, hasil prediksi muncul instan beserta confidence score dan distribusi probabilitas tiap kelas.
- **Dashboard ringkasan** — statistik dataset, akurasi model, dan distribusi spesies.
- **Halaman Evaluasi** — confusion matrix, classification report, feature importance.
- **Halaman Dataset** — informasi sumber data, pembagian train/test, dan distribusi gambar per spesies.
- **Halaman Tentang** — penjelasan metodologi dan deskripsi tiap spesies.
- **Responsif** — tampilannya menyesuaikan layar HP dan desktop.

---

## 🐠 Spesies Ikan yang Didukung

| # | Nama Umum      | Nama Latin                          |
|---|----------------|-------------------------------------|
| 1 | Bandeng        | *Chanos chanos*                     |
| 2 | Senangin       | *Eleutheronema tetradactylum*       |
| 3 | Gulamah        | *Johnius trachycephalus*            |
| 4 | Gulama Putih   | *Nibea albiflora*                   |
| 5 | Nila Mozambik  | *Oreochromis mossambicus*           |
| 6 | Nila           | *Oreochromis niloticus*             |
| 7 | Kembung        | *Rastrelliger faughni*              |
| 8 | Biji Nangka    | *Upeneus moluccensis*               |

---

## 🏗️ Arsitektur Sistem

```
Gambar Input (JPG/PNG/WebP/TIF)
        ↓
Preprocessing OpenCV
  - Resize → 224×224 px
  - Konversi BGR → RGB dan HSV
        ↓
Ekstraksi Fitur Warna (6 fitur)
  [Mean R, Mean G, Mean B, Mean H, Mean S, Mean V]
        ↓
Random Forest Classifier (scikit-learn)
  - n_estimators: disesuaikan saat training
  - Model tersimpan sebagai: model/rf_model.pkl
        ↓
Output: nama spesies + confidence + probabilities
```

---

## ⚙️ Instalasi & Menjalankan Lokal

### Prasyarat

- Python 3.10 atau 3.11
- pip

### Langkah-langkah

```bash
# 1. Clone repository
git clone https://github.com/USERNAME/aqualens.git
cd aqualens

# 2. Buat virtual environment
python -m venv venv

# Aktivasi (Windows)
venv\Scripts\activate

# Aktivasi (macOS/Linux)
source venv/bin/activate

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
python app.py
```

Buka browser dan akses `http://localhost:5000`.

> **Catatan:** Jika file `model/rf_model.pkl` belum ada, aplikasi otomatis berjalan dalam **demo mode** dengan prediksi acak. Jalankan `python train_model.py` terlebih dahulu untuk melatih model nyata (lihat bagian bawah).

---

## 🔧 Melatih Ulang Model

Model Random Forest perlu dilatih dari dataset Fish-gres yang **tidak disertakan** di repository karena ukurannya ~3 GB.

### Download Dataset

Dataset Fish-gres tersedia secara open access di Mendeley Data:

```
https://data.mendeley.com/datasets/76cr3wfhff/1
```

Sitasi dataset:
> Prasetyo, E., et al. (2021). *Fish-gres: Fish Identification Dataset for Traditional Market in Gresik, East Java*. Mendeley Data, V1. DOI: 10.17632/76cr3wfhff.1

### Struktur Folder Dataset

Setelah download dan ekstrak, susun folder `dataset/` seperti berikut di dalam folder proyek:

```
fish_classifier/
└── dataset/
    ├── chanos_chanos/
    │   ├── img001.jpg
    │   ├── img002.jpg
    │   └── ...
    ├── eleutheronema_tetradactylum/
    ├── johnius_trachycephalus/
    ├── nibea_albiflora/
    ├── oreochromis_mossambicus/
    ├── oreochromis_niloticus/
    ├── rastrelliger_faughni/
    └── upeneus_moluccensis/
```

### Jalankan Training

```bash
python train_model.py
```

Script akan menghasilkan dua file:
- `model/rf_model.pkl` — model terlatih
- `model/eval_results.json` — hasil evaluasi untuk ditampilkan di web

---

## 📁 Struktur Folder

```
fish_classifier/
├── app.py                  # Entry point Flask
├── train_model.py          # Script training Random Forest
├── requirements.txt        # Dependensi Python
├── Procfile                # Konfigurasi proses untuk Railway/Heroku
├── .gitignore              # File yang diabaikan git
│
├── model/
│   ├── rf_model.pkl        # Model terlatih (generated, tidak di-commit)
│   └── eval_results.json   # Hasil evaluasi (generated, tidak di-commit)
│
├── dataset/                # Folder dataset (TIDAK di-commit, ukuran ~3 GB)
│   └── ...
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   ├── libs/
│   │   ├── apex-charts/
│   │   └── perfect-scrollbar/
│   └── img/
│       ├── uploads/        # Tempat gambar upload sementara
│       └── ...
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── klasifikasi.html
    ├── evaluasi.html
    ├── dataset.html
    └── tentang.html
```

---

## 🚀 Deployment ke Railway

### Strategi Dataset — Solusi 3 GB vs Limit 512 MB

> Dataset TIDAK diikutsertakan ke Railway. Solusinya adalah **pre-train lokal**, lalu hanya upload model `.pkl` (ukurannya kecil, biasanya 5–50 MB) ke repository.

**Alurnya:**

```
[Lokal] Download dataset → train_model.py → rf_model.pkl + eval_results.json
                                                     ↓
[GitHub] Commit hanya kode + rf_model.pkl + eval_results.json (tanpa dataset/)
                                                     ↓
[Railway] Pull dari GitHub → jalankan gunicorn → deploy selesai
```

### Langkah 1 — Persiapan File Lokal

Pastikan file-file ini sudah ada sebelum push ke GitHub:

```
model/rf_model.pkl          ← wajib ada
model/eval_results.json     ← wajib ada
Procfile                    ← sudah ada di zip
requirements.txt            ← sudah ada di zip
```

Isi `Procfile` (sudah benar dari zip):

```
web: gunicorn app:app
```

### Langkah 2 — Setup GitHub Repository

```bash
# Inisialisasi git di folder fish_classifier/
cd fish_classifier
git init

# Buat file .gitignore dulu (lihat isinya di bagian .gitignore)
# lalu staging semua file
git add .
git commit -m "feat: initial commit AquaLens v13"

# Hubungkan ke GitHub
git remote add origin https://github.com/USERNAME/aqualens.git
git branch -M main
git push -u origin main
```

### Langkah 3 — Deploy di Railway

1. Buka [railway.app](https://railway.app) dan login dengan akun GitHub.
2. Klik **New Project** → **Deploy from GitHub repo**.
3. Pilih repository `aqualens`.
4. Railway otomatis mendeteksi Python dan menjalankan `Procfile`.
5. Tunggu proses build selesai (biasanya 2–5 menit).
6. Setelah deploy berhasil, klik **Settings** → **Domains** → **Generate Domain** untuk mendapatkan URL sementara seperti `aqualens-production.up.railway.app`.

### Langkah 4 — Variabel Lingkungan (Opsional)

Di Railway, buka tab **Variables** dan tambahkan jika diperlukan:

```
FLASK_ENV=production
PORT=8080
```

> Railway otomatis mengatur `PORT`. Gunicorn sudah membacanya via Procfile.

---

## 🌐 Konfigurasi Domain my.id (IDCloudHost)

### Prasyarat

- Sudah memiliki domain `.my.id` yang terdaftar di [idcloudhost.com](https://idcloudhost.com) atau [idlocalhost.com](https://idlocalhost.com).
- Aplikasi sudah berjalan di Railway dan mendapat URL Railway (misal: `aqualens-production.up.railway.app`).

### Langkah 1 — Tambahkan Custom Domain di Railway

1. Di dashboard Railway, buka project kamu.
2. Masuk ke tab **Settings** → **Domains**.
3. Klik **Custom Domain** → ketik domain kamu, misal: `aqualens.my.id`.
4. Railway akan menampilkan **nilai CNAME** yang harus diarahkan, contohnya:
   ```
   CNAME target: aqualens-production.up.railway.app
   ```

### Langkah 2 — Konfigurasi DNS di Panel IDCloudHost

1. Login ke panel domain kamu di **idcloudhost.com** atau **idlocalhost.com**.
2. Buka menu **DNS Management** atau **Kelola DNS** untuk domain `aqualens.my.id`.
3. Tambahkan record DNS berikut:

   | Type  | Name / Host     | Value / Target                              | TTL  |
   |-------|-----------------|---------------------------------------------|------|
   | CNAME | `@` atau `www`  | `aqualens-production.up.railway.app`        | 3600 |

   Jika domain kamu adalah `aqualens.my.id` (tanpa subdomain), pilih `@` sebagai Host.
   Jika domain kamu adalah `www.aqualens.my.id`, pilih `www`.

4. Simpan perubahan DNS.

### Langkah 3 — Tunggu Propagasi DNS

Propagasi DNS biasanya membutuhkan **5–30 menit**, terkadang hingga 24 jam untuk beberapa ISP. Kamu bisa cek status propagasi di [dnschecker.org](https://dnschecker.org).

### Langkah 4 — Verifikasi di Railway

Setelah DNS propagasi selesai, Railway secara otomatis akan menerbitkan **SSL/TLS certificate** (HTTPS) via Let's Encrypt. Kamu tidak perlu konfigurasi SSL manual.

Setelah selesai, aplikasi bisa diakses di:
```
https://aqualens.my.id
```

---

## 📄 Isi .gitignore yang Wajib Ada

Buat file `.gitignore` di root folder proyek dengan isi berikut:

```gitignore
# Dataset — ukuran ~3 GB, tidak perlu di-push
dataset/

# Folder upload sementara
static/img/uploads/

# Virtual environment Python
venv/
env/
.venv/

# Cache Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Environment variables
.env
.env.local

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

> **Penting:** File `model/rf_model.pkl` dan `model/eval_results.json` **tidak** dimasukkan ke `.gitignore` supaya Railway bisa menggunakannya langsung tanpa perlu re-training.

---

## ❓ FAQ

**Q: Kenapa dataset tidak di-push ke GitHub?**

GitHub memiliki batas ukuran file 100 MB per file dan 1 GB per repository (soft limit). Dataset gambar ~3 GB jelas tidak bisa masuk. Solusinya adalah commit hanya model `.pkl` yang sudah dilatih, bukan raw dataset-nya.

**Q: Kenapa Railway bisa jalan tanpa dataset?**

Karena yang dibutuhkan Railway hanya `rf_model.pkl` untuk inferensi. Dataset hanya diperlukan saat *training*, bukan saat *serving*. Training dilakukan sekali di lokal, hasilnya (pkl) yang dikirim ke server.

**Q: Apakah ada cara menyimpan dataset online selain GitHub?**

Bisa. Beberapa opsi yang umum dipakai:
- **Google Drive** atau **OneDrive** (download manual saat dibutuhkan)
- **Hugging Face Datasets** (cocok untuk dataset ML publik)
- **Kaggle Datasets** (jika dataset versi publik)
- **DVC (Data Version Control)** dengan remote storage S3/GCS (untuk tim dan proyek serius)

Untuk keperluan akademik, menyimpan model pkl di repo dan dataset di Google Drive sudah lebih dari cukup.

**Q: Ukuran `rf_model.pkl` seberapa besar?**

Tergantung parameter `n_estimators` saat training. Dengan 100–200 trees dan 6 fitur, biasanya **5–30 MB**. Masih jauh di bawah limit Railway maupun GitHub.

**Q: Apakah bisa deploy gratis di Railway?**

Railway menyediakan plan **Hobby** dengan kredit $5/bulan untuk pengguna baru. Cukup untuk proyek akademik dengan trafik rendah. Pantau penggunaan di dashboard Railway agar tidak melebihi kredit.

---

## 📚 Referensi Dataset

Prasetyo, E., Suciati, N., Fatichah, C., Navastara, D. A., Arifin, A. Z., & Muñoz-Salinas, R. (2021). *Fish-gres: Fish Identification Dataset for Traditional Market in Gresik, East Java*. Mendeley Data, V1. https://doi.org/10.17632/76cr3wfhff.1

---

## 👩‍💻 Kontributor

| Nama | NIM | Program Studi |
|------|-----|---------------|
| Aulia Nazwa Huriah | 301240010 | Teknik Informatika — Universitas Bale Bandung |

---

## 📝 Lisensi

Proyek ini dibuat untuk keperluan akademik. Dataset Fish-gres mengikuti lisensi **CC BY 4.0** dari Mendeley Data.
