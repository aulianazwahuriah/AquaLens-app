"""
=============================================================
  Script Pelatihan Model Random Forest
  Klasifikasi Jenis Ikan Konsumsi Pasar Tradisional
=============================================================
  Dataset  : Fish-gres Dataset (Prasetyo et al., 2021)
             Mendeley Data, DOI: 10.17632/76cr3wfhff.1
             Institut Teknologi Sepuluh Nopember (ITS) Surabaya

  Output   : model/rf_model.pkl  — model terlatih
             model/eval_results.json — hasil evaluasi untuk web

  Cara jalankan:
    python train_model.py
=============================================================
"""

import os
import json
import pickle
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ─────────────────────────────────────────────
# Konfigurasi
# ─────────────────────────────────────────────

DATASET_PATH = 'dataset'
IMG_SIZE     = (224, 224)

# Key = nama folder di dataset/, Value = label numerik
# Urutan ini harus sama persis dengan LABEL_IKAN di app.py
LABEL_KELAS = {
    'chanos_chanos':                0,
    'eleutheronema_tetradactylum':  1,
    'johnius_trachycephalus':       2,
    'nibea_albiflora':              3,
    'oreochromis_mossambicus':      4,
    'oreochromis_niloticus':        5,
    'rastrelliger_faughni':         6,
    'upeneus_moluccensis':          7
}

NAMA_TAMPILAN = [
    'Bandeng', 'Senangin', 'Gulamah', 'Gulama Putih',
    'Nila Mozambik', 'Nila', 'Kembung', 'Biji Nangka'
]

NAMA_FITUR = ['Mean R', 'Mean G', 'Mean B', 'Mean H', 'Mean S', 'Mean V']


# ─────────────────────────────────────────────
# Fungsi Ekstraksi Fitur
# ─────────────────────────────────────────────

def extract_features(image_path):
    """
    Mengekstrak 6 fitur warna dari satu gambar.
    Fitur: [Mean_R, Mean_G, Mean_B] dari RGB + [Mean_H, Mean_S, Mean_V] dari HSV
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    img = cv2.resize(img, IMG_SIZE)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return [
        np.mean(img_rgb[:, :, 0]),
        np.mean(img_rgb[:, :, 1]),
        np.mean(img_rgb[:, :, 2]),
        np.mean(img_hsv[:, :, 0]),
        np.mean(img_hsv[:, :, 1]),
        np.mean(img_hsv[:, :, 2])
    ]


# ─────────────────────────────────────────────
# Langkah 1: Baca Dataset
# ─────────────────────────────────────────────

print("=" * 60)
print("  PELATIHAN MODEL — FishScan RF")
print("  Dataset: Fish-gres, ITS Surabaya (DOI: 10.17632/76cr3wfhff.1)")
print("=" * 60)
print("\n[1/5] Membaca gambar dan mengekstrak fitur warna...")

X = []
y = []
jumlah_per_kelas = {}

for nama_folder, label in LABEL_KELAS.items():
    path_folder = os.path.join(DATASET_PATH, nama_folder)
    if not os.path.exists(path_folder):
        print(f"  [!] Folder tidak ditemukan: {path_folder}")
        continue

    jumlah = 0
    for nama_file in os.listdir(path_folder):
        if not nama_file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')):
            continue
        fitur = extract_features(os.path.join(path_folder, nama_file))
        if fitur is not None:
            X.append(fitur)
            y.append(label)
            jumlah += 1

    jumlah_per_kelas[NAMA_TAMPILAN[label]] = jumlah
    print(f"  [{label}] {NAMA_TAMPILAN[label]:20s}: {jumlah} gambar")

X = np.array(X)
y = np.array(y)
print(f"\n  Total: {len(X)} sampel, {X.shape[1]} fitur, {len(LABEL_KELAS)} kelas")


# ─────────────────────────────────────────────
# Langkah 2: Bagi Data
# ─────────────────────────────────────────────

print("\n[2/5] Membagi data: 80% latih, 20% uji...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"  Latih: {len(X_train)} | Uji: {len(X_test)}")


# ─────────────────────────────────────────────
# Langkah 3: Latih Model
# ─────────────────────────────────────────────

print("\n[3/5] Melatih Random Forest (n_estimators=100, max_depth=10)...")

model = RandomForestClassifier(
    n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)
print("  Model berhasil dilatih.")


# ─────────────────────────────────────────────
# Langkah 4: Evaluasi
# ─────────────────────────────────────────────

print("\n[4/5] Mengevaluasi model...")

y_pred  = model.predict(X_test)
akurasi = accuracy_score(y_test, y_pred)
cm      = confusion_matrix(y_test, y_pred)
report  = classification_report(y_test, y_pred,
                                target_names=NAMA_TAMPILAN,
                                output_dict=True)

print(f"\n  Akurasi: {akurasi * 100:.2f}%")
print("\n  Laporan per kelas:")
print(classification_report(y_test, y_pred, target_names=NAMA_TAMPILAN))
print("  Confusion Matrix:")
print(cm)

# Feature importance dari Random Forest
importances = model.feature_importances_.tolist()


# ─────────────────────────────────────────────
# Langkah 5: Simpan Model + Hasil Evaluasi
# ─────────────────────────────────────────────

print("\n[5/5] Menyimpan model dan hasil evaluasi...")

os.makedirs('model', exist_ok=True)

# Simpan model
with open(os.path.join('model', 'rf_model.pkl'), 'wb') as f:
    pickle.dump(model, f)

# Simpan hasil evaluasi ke JSON untuk ditampilkan di halaman web
eval_data = {
    'akurasi': round(akurasi * 100, 2),
    'jumlah_latih': int(len(X_train)),
    'jumlah_uji': int(len(X_test)),
    'jumlah_per_kelas': jumlah_per_kelas,
    'confusion_matrix': cm.tolist(),
    'nama_kelas': NAMA_TAMPILAN,
    'feature_importance': {
        'nama_fitur': NAMA_FITUR,
        'nilai': [round(v, 6) for v in importances]
    },
    'classification_report': {
        kelas: {
            'precision': round(report[kelas]['precision'] * 100, 1),
            'recall':    round(report[kelas]['recall'] * 100, 1),
            'f1_score':  round(report[kelas]['f1-score'] * 100, 1),
            'support':   int(report[kelas]['support'])
        }
        for kelas in NAMA_TAMPILAN
    }
}

with open(os.path.join('model', 'eval_results.json'), 'w') as f:
    json.dump(eval_data, f, indent=2, ensure_ascii=False)

print("  Model   : model/rf_model.pkl")
print("  Evaluasi: model/eval_results.json")
print("\n" + "=" * 60)
print("  Selesai! Jalankan python app.py untuk memulai.")
print("=" * 60)
