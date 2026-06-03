/**
 * OceanScan — main.js
 * ============================================================
 * Menangani:
 *   - Toggle sidebar (mobile, Bootstrap 5)
 *   - Upload file, drag-and-drop, preview placeholder
 *   - Switch tampilan: form upload <-> hasil identifikasi
 *   - Kirim gambar ke API /api/predict dan render hasilnya
 * ============================================================
 */

(function () {
  'use strict';

  /* ============================================================
     SIDEBAR — toggle buka/tutup untuk tampilan mobile
  ============================================================ */

  var sidebar        = document.getElementById('sidebar');
  var sidebarOverlay = document.getElementById('sidebarOverlay');
  var hamburgerBtn   = document.getElementById('hamburgerBtn');

  function openSidebar() {
    if (!sidebar) return;
    sidebar.classList.add('open');
    if (sidebarOverlay) { sidebarOverlay.classList.add('active'); }
  }

  function closeSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    if (sidebarOverlay) { sidebarOverlay.classList.remove('active'); }
  }

  if (hamburgerBtn) hamburgerBtn.addEventListener('click', function () {
    sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
  });

  if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeSidebar);

  /* ============================================================
     CEK HALAMAN — keluar jika bukan halaman klasifikasi
  ============================================================ */

  var viewUpload = document.getElementById('viewUpload');
  var viewResult = document.getElementById('viewResult');
  if (!viewUpload) return;

  /* ─── Referensi elemen upload ─────────────────────────── */
  var fileInput       = document.getElementById('fileInput');
  var uploadZone      = document.getElementById('uploadZone');
  var previewSection  = document.getElementById('previewSection');
  var previewFilename = document.getElementById('previewFilename');
  var previewSize     = document.getElementById('previewSize');
  var clearBtn        = document.getElementById('clearBtn');
  var identifyBtn     = document.getElementById('identifyBtn');
  var loadingOverlay  = document.getElementById('loadingOverlay');

  var selectedFile = null;

  /* Emoji per indeks kelas (fallback jika tidak ada gambar) */
  var FISH_EMOJI = ['🐟', '🐠', '🐡', '🐟', '🐠', '🐟', '🐡', '🐠'];

  /* ─── Utilitas ─────────────────────────────────────────── */

  function formatBytes(bytes) {
    if (bytes < 1024)    return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  }

  function setText(id, value) {
    var el = document.getElementById(id);
    if (el) el.textContent = value || '';
  }

  /* ============================================================
     PREVIEW — tampilkan informasi file tanpa render gambar
     Gambar asli hanya ditampilkan di hasil setelah identifikasi
     (dikirim kembali oleh server dalam format JPEG base64)
  ============================================================ */

  function showPreview(file) {
    selectedFile = file;

    /* Tampilkan info file (nama + ukuran) — tanpa render gambar */
    if (previewFilename) previewFilename.textContent = file.name;
    if (previewSize)     previewSize.textContent     = formatBytes(file.size);

    /* Sembunyikan drop zone, tampilkan section preview */
    if (uploadZone)    uploadZone.classList.add('d-none');
    if (previewSection) previewSection.classList.remove('d-none');
    if (identifyBtn)   identifyBtn.disabled = false;
  }

  /* ─── Reset kembali ke tampilan form upload ────────────── */

  function resetToUpload() {
    selectedFile = null;

    if (previewFilename) previewFilename.textContent = '';
    if (previewSize)     previewSize.textContent     = '';
    if (fileInput)       fileInput.value             = '';

    if (uploadZone)    uploadZone.classList.remove('d-none');
    if (previewSection) previewSection.classList.add('d-none');
    if (identifyBtn)   identifyBtn.disabled = true;

    /* Kembali ke view upload */
    if (viewResult) viewResult.classList.add('d-none');
    if (viewUpload) viewUpload.classList.remove('d-none');

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /* ─── Event: pilih file lewat input ────────────────────── */

  if (fileInput) {
    fileInput.addEventListener('change', function () {
      if (this.files && this.files[0]) showPreview(this.files[0]);
    });
  }

  if (clearBtn) clearBtn.addEventListener('click', resetToUpload);

  /* ─── Event: drag and drop ──────────────────────────────── */

  if (uploadZone) {
    uploadZone.addEventListener('dragover', function (e) {
      e.preventDefault(); uploadZone.classList.add('drag-over');
    });
    uploadZone.addEventListener('dragleave', function () {
      uploadZone.classList.remove('drag-over');
    });
    uploadZone.addEventListener('drop', function (e) {
      e.preventDefault();
      uploadZone.classList.remove('drag-over');
      var file = e.dataTransfer.files[0];
      if (file && /\.(jpg|jpeg|png|webp|tif|tiff)$/i.test(file.name)) {
        showPreview(file);
      }
    });
  }

  /* ─── Event: tombol Identifikasi Lagi ──────────────────── */

  ['identifyAgainBtn', 'identifyAgainBtn2'].forEach(function (id) {
    var btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', resetToUpload);
  });

  /* ─── Event: tombol Identifikasi Sekarang ───────────────── */

  if (identifyBtn) identifyBtn.addEventListener('click', runIdentify);

  /* ============================================================
     API CALL — kirim gambar ke /api/predict, terima JSON
  ============================================================ */

  function runIdentify() {
    if (!selectedFile) return;

    var formData = new FormData();
    formData.append('file', selectedFile);

    if (loadingOverlay) loadingOverlay.classList.add('active');

    fetch('/api/predict', { method: 'POST', body: formData })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (loadingOverlay) loadingOverlay.classList.remove('active');
        if (data.error)     { alert('Error: ' + data.error); return; }
        renderResult(data);
      })
      .catch(function (err) {
        if (loadingOverlay) loadingOverlay.classList.remove('active');
        console.error('API error:', err);
        alert('Terjadi kesalahan saat menghubungi server.');
      });
  }

  /* ============================================================
     RENDER HASIL — isi semua elemen hasil dengan data prediksi
  ============================================================ */

  function renderResult(data) {

    /* Foto dianalisis: server selalu mengembalikan JPEG base64 */
    var resultImg = document.getElementById('resultImg');
    if (resultImg && data.preview_url) {
      resultImg.src = data.preview_url;
      resultImg.style.display = 'block';
    }

    /* Info file */
    setText('resultFilename', selectedFile ? selectedFile.name : '');
    setText('resultFilesize', selectedFile ? formatBytes(selectedFile.size) : '');

    /* Informasi spesies */
    setText('resultName',      data.nama);
    setText('resultLatin',     data.latin);
    setText('resultHabitat',   data.habitat_detail || data.habitat);
    setText('resultCiri',      data.ciri);
    setText('resultGizi',      data.gizi);
    setText('resultDeskripsi', data.deskripsi || '');

    var emojiEl = document.getElementById('resultEmoji');
    if (emojiEl) emojiEl.textContent = FISH_EMOJI[data.predicted_class] || '🐟';

    /* Confidence bar animasi */
    var pctEl = document.getElementById('confidencePct');
    var barEl = document.getElementById('confidenceBar');
    if (pctEl) pctEl.textContent = data.confidence + '%';
    if (barEl) { barEl.style.width = '0%'; setTimeout(function () { barEl.style.width = data.confidence + '%'; }, 80); }

    /* Grid 6 fitur warna */
    renderFeatures(data.features);

    /* Bar probabilitas per kelas */
    renderProbabilities(data.probabilities, data.nama_kelas, data.predicted_class);

    /* Fakta menarik (poin-poin teks, tanpa ikon/gambar) */
    renderFaktaMenarik(data.predicted_class);

    /* Switch tampilan */
    if (viewUpload) viewUpload.classList.add('d-none');
    if (viewResult) {
      viewResult.classList.remove('d-none');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  /* ─── Render: 6 fitur warna ─────────────────────────────── */

  function renderFeatures(features) {
    var grid = document.getElementById('featureGrid');
    if (!grid || !features) return;
    grid.innerHTML = '';
    for (var i = 0; i < features.values.length; i++) {
      var item = document.createElement('div');
      item.className = 'feature-item';
      item.innerHTML =
        '<div class="feature-val">' + features.values[i].toFixed(1) + '</div>' +
        '<div class="feature-lbl">' + features.names[i] + '</div>';
      grid.appendChild(item);
    }
  }

  /* ─── Render: bar probabilitas per kelas ───────────────── */

  function renderProbabilities(probs, names, topClass) {
    var list = document.getElementById('probList');
    if (!list) return;
    list.innerHTML = '';

    var combined = probs.map(function (p, i) { return { p: p, n: names[i], i: i }; });
    combined.sort(function (a, b) { return b.p - a.p; });

    combined.forEach(function (item) {
      var isTop = (item.i === topClass);
      var row   = document.createElement('div');
      row.className = 'prob-row';
      row.innerHTML =
        '<span class="prob-label' + (isTop ? ' prob-label-top' : '') + '">' + item.n + '</span>' +
        '<div class="prob-bar-wrap">' +
          '<div class="prob-bar-fill' + (isTop ? ' is-top' : '') +
          '" style="width:0%" data-pct="' + item.p + '"></div>' +
        '</div>' +
        '<span class="prob-pct' + (isTop ? ' prob-pct-top' : '') + '">' + item.p.toFixed(1) + '%</span>';
      list.appendChild(row);
    });

    setTimeout(function () {
      list.querySelectorAll('.prob-bar-fill').forEach(function (bar) {
        bar.style.width = bar.getAttribute('data-pct') + '%';
      });
    }, 100);
  }

  /* ─── Render: fakta menarik dalam poin-poin teks ──────── */
  /* Tidak menggunakan ikon/gambar ikan — hanya teks faktual */

  function renderFaktaMenarik(classIdx) {
    var panel = document.getElementById('habitatPanel');
    if (!panel) return;

    /* Data fakta per spesies: array of string poin */
    var FAKTA = [
      /* 0 Bandeng */
      [
        'Bandeng adalah ikan budidaya tambak paling populer di Indonesia, terutama di Jawa dan Sulawesi.',
        'Duri halusnya yang banyak membuat pengolahan menjadi tantangan tersendiri; presto adalah cara umum agar duri lunak.',
        'Kandungan protein bandeng mencapai 20-24 gram per 100 gram daging, menjadikannya sumber protein hewani yang baik.',
        'Bandeng dapat hidup di air tawar, payau, maupun laut, sehingga mudah dibudidayakan di berbagai kondisi.'
      ],
      /* 1 Senangin */
      [
        'Senangin atau Fourfinger Threadfin memiliki empat hingga lima helai sirip dada yang memanjang seperti benang sebagai ciri khasnya.',
        'Ikan ini merupakan predator aktif yang memangsa ikan-ikan kecil dan udang di perairan muara.',
        'Daging Senangin berwarna putih, teksturnya lembut, dan rasanya gurih sehingga cocok untuk berbagai metode memasak.',
        'Nilai jualnya cukup tinggi di pasar tradisional Jawa Timur karena kelangkaannya dibanding ikan laut biasa.'
      ],
      /* 2 Gulamah */
      [
        'Gulamah termasuk ikan demersal, artinya ia hidup dan mencari makan di dekat dasar perairan berlumpur.',
        'Ikan ini mampu menghasilkan suara menggunakan otot di sekitar kantung udara, unik di antara ikan laut.',
        'Gulamah sering dijual segar di pasar pesisir Jawa Timur dan menjadi bahan dasar kerupuk ikan tradisional.',
        'Ukurannya yang sedang (20-40 cm) membuatnya mudah diolah utuh maupun dibelah sebagai ikan goreng.'
      ],
      /* 3 Gulama Putih */
      [
        'Gulama Putih berkerabat dekat dengan Gulamah tetapi memiliki warna tubuh yang lebih cerah dan keperakan.',
        'Spesies ini hidup di perairan pantai berpasir dan berlumpur pada kedalaman 10-80 meter.',
        'Dagingnya relatif sedikit berduri besar dibanding beberapa ikan demersal lain, memudahkan konsumsi.',
        'Gulama Putih termasuk dalam famili Sciaenidae yang juga dikenal sebagai "ikan drum" karena kemampuan bersuaranya.'
      ],
      /* 4 Nila Mozambik */
      [
        'Nila Mozambik (Oreochromis mossambicus) berasal dari sungai-sungai di Mozambik dan Afrika Selatan.',
        'Warnanya lebih gelap dengan bercak kehitaman di tepi sirip ekor, berbeda dari Nila biasa yang lebih terang.',
        'Spesies ini sangat toleran terhadap kondisi air dengan kadar oksigen rendah dan salinitas tinggi.',
        'Di Indonesia, Nila Mozambik menjadi induk silang untuk menghasilkan varietas Nila unggul seperti Nila GIFT.'
      ],
      /* 5 Nila */
      [
        'Nila (Oreochromis niloticus) adalah ikan budidaya air tawar dengan produksi terbesar di Indonesia.',
        'Ikan ini omnivora dan dapat memakan fitoplankton, lumut, dan pakan buatan, sehingga biaya produksi rendah.',
        'Kandungan proteinnya sekitar 26 gram per 100 gram, dengan kandungan lemak yang rendah dan kaya omega-3.',
        'Nila dapat dipanen dalam waktu 4-6 bulan dari benih hingga ukuran konsumsi 300-500 gram per ekor.'
      ],
      /* 6 Kembung */
      [
        'Kembung (Rastrelliger spp.) adalah sumber omega-3 paling terjangkau dan mudah didapat di Indonesia.',
        'Kandungan DHA dan EPA per 100 gram kembung setara dengan salmon, namun harganya jauh lebih murah.',
        'Ikan ini hidup bergerombol di lapisan permukaan laut tropis dan ditangkap dengan jaring pukat cincin.',
        'Kembung sangat mudah rusak sehingga biasanya dijual segar di hari yang sama dengan penangkapannya.'
      ],
      /* 7 Biji Nangka */
      [
        'Biji Nangka (Upeneus moluccensis) mendapat namanya dari warna merah-jingga tubuhnya yang menyerupai biji nangka.',
        'Ikan ini termasuk Mullidae (goatfish) yang memiliki sepasang sungut di dagu untuk mendeteksi makanan di dasar laut.',
        'Habitatnya di sekitar terumbu karang dan substrat berpasir pada kedalaman 10-50 meter.',
        'Biji Nangka populer sebagai ikan goreng di warung makan pesisir Jawa Timur karena ukurannya yang pas untuk satu porsi.'
      ]
    ];

    var poin = FAKTA[classIdx] || FAKTA[0];

    /* Render sebagai daftar poin tanpa ikon/gambar */
    var html = '<ul style="padding-left:0; list-style:none; margin:0; display:flex; flex-direction:column; gap:10px;">';
    poin.forEach(function (p) {
      html +=
        '<li style="display:flex; gap:10px; align-items:flex-start; font-size:13px; color:var(--text-secondary); line-height:1.65;">' +
          '<span style="flex-shrink:0; margin-top:4px; width:7px; height:7px; border-radius:50%; background:var(--primary); display:inline-block;"></span>' +
          '<span>' + p + '</span>' +
        '</li>';
    });
    html += '</ul>';

    panel.innerHTML = html;
  }

})();
