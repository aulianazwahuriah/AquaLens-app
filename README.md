# 🐟 AquaLens — Klasifikasi Jenis Ikan Konsumsi

**AquaLens** adalah aplikasi web berbasis Flask yang mengklasifikasikan 8 spesies ikan konsumsi pasar tradisional menggunakan algoritma **Random Forest** dengan ekstraksi fitur warna (RGB + HSV). Model dilatih dari dataset Fish-gres (ITS Surabaya, Mendeley Data, DOI: 10.17632/76cr3wfhff.1).

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
git clone https://github.com/aulianazwahuriah/aqualens-app.git
cd aqualens-app

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

## 📚 Referensi Dataset

Prasetyo, E., Suciati, N., Fatichah, C., Navastara, D. A., Arifin, A. Z., & Muñoz-Salinas, R. (2021). *Fish-gres: Fish Identification Dataset for Traditional Market in Gresik, East Java*. Mendeley Data, V1. https://doi.org/10.17632/76cr3wfhff.1

---

## 👤 Developer

| Profile | Detail |
| :--- | :--- |
| **Name** | Aulia Nazwa Huriah |
| **NIM** | 301240010 |
| **Education** | Teknik Informatika – Universitas Bale Bandung |
| **LinkedIn** | [linkedin.com/in/username-kamu](#) |

---

## 📝 Lisensi

Proyek ini dibuat untuk keperluan akademik. Dataset Fish-gres mengikuti lisensi **CC BY 4.0** dari Mendeley Data.
