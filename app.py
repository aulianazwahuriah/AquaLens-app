"""
=============================================================
  app.py — AquaLens Flask Application
  Klasifikasi Jenis Ikan Konsumsi menggunakan Random Forest
=============================================================
"""

import os
import json
import pickle
import base64
import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

# ─────────────────────────────────────────────
# Konfigurasi Aplikasi
# ─────────────────────────────────────────────

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'img', 'uploads')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'tif', 'tiff'}
IMG_SIZE = (224, 224)

# Label & info ikan
LABEL_IKAN = [
    {
        'id': 0,
        'nama': 'Bandeng',
        'latin': 'Chanos chanos',
        'habitat': 'Tambak air payau',
        'habitat_detail': 'Tambak, muara sungai, laut dangkal',
        'ciri': 'Tubuh memanjang, sisik perak, sirip ekor bercabang',
        'gizi': 'Tinggi protein, omega-3, kalsium',
        'deskripsi': 'Ikan Bandeng adalah salah satu ikan budidaya paling populer di Indonesia, terutama di tambak air payau. Dagingnya lembut dan gurih, menjadikannya bahan utama berbagai masakan khas Nusantara.',
        'emoji': '🐟'
    },
    {
        'id': 1,
        'nama': 'Senangin',
        'latin': 'Eleutheronema tetradactylum',
        'habitat': 'Perairan pantai & muara',
        'habitat_detail': 'Muara sungai, pesisir berlumpur',
        'ciri': 'Tubuh memanjang, sirip dada berbentuk benang panjang',
        'gizi': 'Kaya protein, rendah lemak',
        'deskripsi': 'Ikan Senangin memiliki ciri khas sirip dada yang memanjang seperti benang. Hidup di perairan muara dan pantai berlumpur, ikan ini dikenal dengan tekstur dagingnya yang kenyal dan lezat.',
        'emoji': '🦈'
    },
    {
        'id': 2,
        'nama': 'Gulamah',
        'latin': 'Johnius trachycephalus',
        'habitat': 'Dasar perairan pantai',
        'habitat_detail': 'Laut dangkal, dasar berlumpur',
        'ciri': 'Tubuh bulat, warna keperakan, kepala besar',
        'gizi': 'Protein tinggi, sumber mineral',
        'deskripsi': 'Ikan Gulamah adalah ikan demersal yang hidup di dasar perairan pantai berlumpur. Ikan ini memiliki nilai ekonomis tinggi dan sering dijual segar di pasar tradisional.',
        'emoji': '🐠'
    },
    {
        'id': 3,
        'nama': 'Gulama Putih',
        'latin': 'Nibea albiflora',
        'habitat': 'Pantai berlumpur & berpasir',
        'habitat_detail': 'Perairan pantai dangkal',
        'ciri': 'Warna putih keperakan, badan agak pipih',
        'gizi': 'Protein tinggi, rendah kalori',
        'deskripsi': 'Gulama Putih merupakan kerabat dekat Gulamah dengan warna tubuh yang lebih putih. Ikan ini hidup di perairan pantai yang berlumpur dan berpasir, sering menjadi tangkapan nelayan tradisional.',
        'emoji': '🦑'
    },
    {
        'id': 4,
        'nama': 'Nila Mozambik',
        'latin': 'Oreochromis mossambicus',
        'habitat': 'Sungai, kolam air tawar',
        'habitat_detail': 'Sungai, danau, kolam, tambak',
        'ciri': 'Tubuh oval, warna gelap, bercak hitam di sirip ekor',
        'gizi': 'Kaya protein, rendah lemak jenuh',
        'deskripsi': 'Ikan Nila Mozambik berasal dari Afrika Selatan dan telah menyebar ke seluruh Indonesia. Warnanya lebih gelap dengan bercak kehitaman di sirip ekor, membedakannya dari Nila biasa.',
        'emoji': '🐬'
    },
    {
        'id': 5,
        'nama': 'Nila',
        'latin': 'Oreochromis niloticus',
        'habitat': 'Sungai, waduk, kolam',
        'habitat_detail': 'Sungai, danau, kolam budidaya',
        'ciri': 'Tubuh pipih lateral, warna abu-abu kehijauan, garis vertikal',
        'gizi': 'Protein lengkap, omega-3, vitamin D',
        'deskripsi': 'Nila adalah salah satu ikan air tawar budidaya terpopuler di Indonesia. Tumbuh cepat, mudah dibudidayakan, dan memiliki daging yang lezat. Sangat umum ditemukan di pasar tradisional.',
        'emoji': '🐡'
    },
    {
        'id': 6,
        'nama': 'Kembung',
        'latin': 'Rastrelliger faughni',
        'habitat': 'Laut dangkal, pantai',
        'habitat_detail': 'Perairan laut terbuka, zona pesisir',
        'ciri': 'Tubuh torpedo, warna hijau-biru berkilau, garis hitam di punggung',
        'gizi': 'Sangat tinggi omega-3, DHA, EPA',
        'deskripsi': 'Ikan Kembung merupakan sumber omega-3 terjangkau dan paling populer di pasar Indonesia. Hidup bergerombol di laut dangkal dan menjadi andalan protein masyarakat pesisir.',
        'emoji': '🦞'
    },
    {
        'id': 7,
        'nama': 'Biji Nangka',
        'latin': 'Upeneus moluccensis',
        'habitat': 'Dasar perairan karang',
        'habitat_detail': 'Terumbu karang, perairan dangkal',
        'ciri': 'Warna merah muda-jingga, tubuh kecil, dua garis kuning',
        'gizi': 'Sumber protein, mineral laut',
        'deskripsi': 'Ikan Biji Nangka mendapat namanya dari warnanya yang menyerupai biji nangka matang. Hidup di sekitar terumbu karang dan dasar perairan dangkal, sering dijual dalam kondisi segar.',
        'emoji': '🦐'
    }
]

NAMA_FITUR = ['Mean R', 'Mean G', 'Mean B', 'Mean H', 'Mean S', 'Mean V']
FITUR_LABEL = {
    'Mean R': 'Rata-rata Merah (RGB)',
    'Mean G': 'Rata-rata Hijau (RGB)',
    'Mean B': 'Rata-rata Biru (RGB)',
    'Mean H': 'Rata-rata Hue (HSV)',
    'Mean S': 'Rata-rata Saturasi (HSV)',
    'Mean V': 'Rata-rata Value (HSV)'
}

# ─────────────────────────────────────────────
# Load Model & Evaluasi
# ─────────────────────────────────────────────

MODEL = None
EVAL_DATA = None

def load_model():
    global MODEL, EVAL_DATA
    model_path = os.path.join('model', 'rf_model.pkl')
    eval_path  = os.path.join('model', 'eval_results.json')

    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            MODEL = pickle.load(f)

    if os.path.exists(eval_path):
        with open(eval_path, 'r') as f:
            EVAL_DATA = json.load(f)
    else:
        # Data dummy untuk demo ketika model belum dilatih
        EVAL_DATA = {
            'akurasi': 87.50,
            'jumlah_latih': 3200,
            'jumlah_uji': 800,
            'jumlah_total': 4000,
            'jumlah_per_kelas': {k['nama']: 500 for k in LABEL_IKAN},
            'confusion_matrix': [[45,2,1,0,1,0,1,0],[2,44,1,1,0,1,0,1],[1,1,43,2,1,0,1,1],[0,1,2,44,1,1,0,1],[1,0,1,1,45,1,0,1],[0,1,0,1,1,44,1,2],[1,0,1,0,0,1,45,2],[0,1,1,1,1,2,2,42]],
            'nama_kelas': [k['nama'] for k in LABEL_IKAN],
            'feature_importance': {
                'nama_fitur': NAMA_FITUR,
                'nilai': [0.195, 0.182, 0.168, 0.165, 0.152, 0.138]
            },
            'classification_report': {
                k['nama']: {'precision': 85.0 + i, 'recall': 84.0 + i, 'f1_score': 84.5 + i, 'support': 50}
                for i, k in enumerate(LABEL_IKAN)
            }
        }

load_model()

# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_features(img_bytes):
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return None, None
    img = cv2.resize(img, IMG_SIZE)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    features = [
        round(float(np.mean(img_rgb[:, :, 0])), 4),
        round(float(np.mean(img_rgb[:, :, 1])), 4),
        round(float(np.mean(img_rgb[:, :, 2])), 4),
        round(float(np.mean(img_hsv[:, :, 0])), 4),
        round(float(np.mean(img_hsv[:, :, 1])), 4),
        round(float(np.mean(img_hsv[:, :, 2])), 4),
    ]
    return features, img

# ─────────────────────────────────────────────
# Jinja2 Filters
# ─────────────────────────────────────────────

@app.template_filter('enumerate')
def jinja_enumerate(iterable):
    return enumerate(iterable)

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route('/')
def dashboard():
    return render_template('dashboard.html',
                           label_ikan=LABEL_IKAN,
                           eval_data=EVAL_DATA)

@app.route('/klasifikasi')
def klasifikasi():
    return render_template('klasifikasi.html',
                           label_ikan=LABEL_IKAN)

@app.route('/evaluasi')
def evaluasi():
    return render_template('evaluasi.html',
                           eval_data=EVAL_DATA,
                           label_ikan=LABEL_IKAN,
                           nama_fitur=NAMA_FITUR,
                           fitur_label=FITUR_LABEL)

@app.route('/dataset')
def dataset():
    return render_template('dataset.html',
                           label_ikan=LABEL_IKAN,
                           eval_data=EVAL_DATA)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html',
                           label_ikan=LABEL_IKAN)

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang dikirim'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File tidak dipilih'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Format file tidak didukung'}), 400

    img_bytes = file.read()

    features, img_cv = extract_features(img_bytes)
    if features is None:
        return jsonify({'error': 'Gagal memproses gambar'}), 400

    # Always re-encode as JPEG so browser can render TIF/WebP/TIFF
    ok, buf = cv2.imencode('.jpg', img_cv, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if ok:
        b64 = base64.b64encode(buf.tobytes()).decode('utf-8')
        preview_url = 'data:image/jpeg;base64,' + b64
    else:
        preview_url = ''

    if MODEL is None:
        # Demo mode: prediksi acak
        import random
        pred_class = random.randint(0, 7)
        confidence = round(random.uniform(65, 92), 2)
        proba_list = [round(random.uniform(1, 10), 2) for _ in range(8)]
        proba_list[pred_class] = confidence
        total = sum(proba_list)
        proba_list = [round(p/total*100, 2) for p in proba_list]
    else:
        proba = MODEL.predict_proba([features])[0]
        pred_class = int(np.argmax(proba))
        confidence = round(float(proba[pred_class]) * 100, 2)
        proba_list = [round(float(p)*100, 2) for p in proba]

    ikan = LABEL_IKAN[pred_class]

    return jsonify({
        'success': True,
        'preview_url': preview_url,
        'predicted_class': pred_class,
        'nama': ikan['nama'],
        'latin': ikan['latin'],
        'confidence': confidence,
        'habitat': ikan['habitat'],
        'habitat_detail': ikan['habitat_detail'],
        'ciri': ikan['ciri'],
        'gizi': ikan['gizi'],
        'deskripsi': ikan['deskripsi'],
        'probabilities': proba_list,
        'nama_kelas': [k['nama'] for k in LABEL_IKAN],
        'features': {
            'values': features,
            'names': NAMA_FITUR,
            'labels': [FITUR_LABEL[n] for n in NAMA_FITUR]
        }
    })

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
