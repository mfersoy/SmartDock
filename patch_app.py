import re

with open("static/js/app.js", "r") as f:
    content = f.read()

# 1. Update mockChecks
old_mock = content.split("let verificationHistory")[0]

new_mock = """// Global Constants
const CONFIDENCE_THRESHOLD = 80;

// Default bank check presets matching mock data scenarios
const mockChecks = [
  {
    id: "CHK-1001",
    dokuman_tipi: "CEK",
    bankName: "First United Bank",
    tint: "none",
    tutar_uyumlu_mu: true,
    veri: {
      cek_no: "1001",
      banka_sube: "First United Bank - 123 Financial Way, NY",
      kesideci: "JOHN DOE",
      keside_tarihi: "2026-07-15",
      tutar_rakam: "$ 5,420.00",
      tutar_yazi: "Five Thousand Four Hundred Twenty Dollars",
      tutar_uyumlu_mu: true
    },
    confidence_scores: {
      cek_no: 98,
      banka_sube: 95,
      kesideci: 92,
      keside_tarihi: 85,
      tutar_rakam: 99,
      tutar_yazi: 88
    },
    coords: {
      cek_no: { left: 71.5, top: 11.5, width: 17, height: 5.5 },
      banka_sube: { left: 12.5, top: 31, width: 38, height: 10 },
      kesideci: { left: 12.5, top: 41, width: 32, height: 6 },
      keside_tarihi: { left: 71.5, top: 15.5, width: 17, height: 5.5 },
      tutar_rakam: { left: 71.5, top: 41, width: 17, height: 6 },
      tutar_yazi: { left: 12.5, top: 50, width: 60, height: 6 }
    }
  },
  {
    id: "NSS-2039",
    dokuman_tipi: "NOTER_SATIS_SOZLESMESI",
    bankName: "İstanbul 14. Noterliği",
    tint: "grayscale(100%)",
    tutar_uyumlu_mu: true,
    veri: {
      noterlik_adi: "İstanbul 14. Noterliği",
      sozlesme_no: "20394",
      islem_tarihi: "2026-07-30",
      plaka_no: "34 ABC 123",
      marka_model: "Volkswagen Golf",
      sasi_no: "WVGZZZ123456789",
      motor_no: "CJZ123456",
      satis_bedeli: "₺ 850.000,00",
      satici_ad_soyad: "AHMET YILMAZ",
      alici_ad_soyad: "MEHMET KAYA",
      vekil_ad_soyad: null
    },
    confidence_scores: {
      noterlik_adi: 98, sozlesme_no: 95, islem_tarihi: 90, plaka_no: 92,
      marka_model: 95, sasi_no: 88, motor_no: 85, satis_bedeli: 98,
      satici_ad_soyad: 90, alici_ad_soyad: 95, vekil_ad_soyad: 0
    },
    coords: {}
  },
  {
    id: "CHK-45829",
    dokuman_tipi: "CEK",
    bankName: "Garanti BBVA",
    tint: "hue-rotate(110deg) saturate(1.1)",
    tutar_uyumlu_mu: true,
    veri: {
      cek_no: "4582910",
      banka_sube: null, // Test case representing unreadable (null) values
      kesideci: "ASYA TEKSTİL SAN. VE TİC. LTD. ŞTİ.",
      keside_tarihi: "2026-07-30",
      tutar_rakam: "₺ 150.000,00",
      tutar_yazi: "YüzElliBin TürkLirası",
      tutar_uyumlu_mu: true
    },
    confidence_scores: {
      cek_no: 97, banka_sube: 0, kesideci: 91, keside_tarihi: 89, tutar_rakam: 99, tutar_yazi: 74
    },
    coords: {
      cek_no: { left: 71.5, top: 11.5, width: 17, height: 5.5 },
      banka_sube: { left: 12.5, top: 31, width: 38, height: 10 },
      kesideci: { left: 12.5, top: 41, width: 32, height: 6 },
      keside_tarihi: { left: 71.5, top: 15.5, width: 17, height: 5.5 },
      tutar_rakam: { left: 71.5, top: 41, width: 17, height: 6 },
      tutar_yazi: { left: 12.5, top: 50, width: 60, height: 6 }
    }
  },
  {
    id: "CHK-88930",
    dokuman_tipi: "CEK",
    bankName: "Yapı Kredi",
    tint: "hue-rotate(240deg) saturate(1.2)",
    tutar_uyumlu_mu: false,
    veri: {
      cek_no: "8893021",
      banka_sube: "Yapı Kredi - Maslak Şubesi",
      kesideci: "MEHMET YILMAZ",
      keside_tarihi: "2026-08-15",
      tutar_rakam: "₺ 45.750,00",
      tutar_yazi: "KırkBeşBinYediYüz TürkLirası",
      tutar_uyumlu_mu: false
    },
    confidence_scores: {
      cek_no: 96, banka_sube: 82, kesideci: 94, keside_tarihi: 76, tutar_rakam: 98, tutar_yazi: 60
    },
    coords: {
      cek_no: { left: 71.5, top: 11.5, width: 17, height: 5.5 },
      banka_sube: { left: 12.5, top: 31, width: 38, height: 10 },
      kesideci: { left: 12.5, top: 41, width: 32, height: 6 },
      keside_tarihi: { left: 71.5, top: 15.5, width: 17, height: 5.5 },
      tutar_rakam: { left: 71.5, top: 41, width: 17, height: 6 },
      tutar_yazi: { left: 12.5, top: 50, width: 60, height: 6 }
    }
  }
];

"""
content = new_mock + "// Seeded verification history log list" + content.split("// Seeded verification history log list")[1]


content = content.replace("activeCheckData.fields", "activeCheckData.veri")
content = content.replace("activeCheckData.tutar_uyumlu_mu", "(activeCheckData.veri.tutar_uyumlu_mu ?? true)")


load_check_replacement = """// Binds data structure to UI fields
function renderFormFields(dokuman_tipi) {
  const formEl = document.getElementById('ocr-form');
  formEl.innerHTML = '';

  const schemaCek = [
    { key: 'cek_no', label: 'Çek Numarası', icon: 'hash' },
    { key: 'banka_sube', label: 'Banka ve Şube Adı', icon: 'landmark' },
    { key: 'kesideci', label: 'Keşideci', icon: 'user' },
    { key: 'keside_tarihi', label: 'Keşide Tarihi', icon: 'calendar' },
    { key: 'tutar_rakam', label: 'Rakamla Tutar', icon: 'circle-dollar-sign' },
    { key: 'tutar_yazi', label: 'Yazıyla Tutar', icon: 'file-text' }
  ];

  const schemaNoter = [
    { key: 'noterlik_adi', label: 'Noterlik Adı', icon: 'landmark' },
    { key: 'sozlesme_no', label: 'Sözleşme / Yevmiye No', icon: 'hash' },
    { key: 'islem_tarihi', label: 'İşlem Tarihi', icon: 'calendar' },
    { key: 'plaka_no', label: 'Plaka No', icon: 'car' },
    { key: 'marka_model', label: 'Marka ve Model', icon: 'tag' },
    { key: 'sasi_no', label: 'Şasi No', icon: 'key' },
    { key: 'motor_no', label: 'Motor No', icon: 'settings' },
    { key: 'satis_bedeli', label: 'Satış Bedeli', icon: 'circle-dollar-sign' },
    { key: 'satici_ad_soyad', label: 'Satıcı Ad Soyad', icon: 'user-minus' },
    { key: 'alici_ad_soyad', label: 'Alıcı Ad Soyad', icon: 'user-plus' },
    { key: 'vekil_ad_soyad', label: 'Vekil Ad Soyad', icon: 'user' }
  ];

  const schema = (dokuman_tipi === "NOTER_SATIS_SOZLESMESI") ? schemaNoter : schemaCek;

  schema.forEach(field => {
    const div = document.createElement('div');
    div.className = "group relative flex items-center justify-between bg-slate-900/30 border border-slate-800/60 p-4 rounded-xl hover:border-slate-700/80 transition-all duration-150";
    div.innerHTML = `
      <div class="w-full flex flex-col md:flex-row md:items-center gap-4">
        <label for="input-${field.key}" class="w-full md:w-1/4 text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
          <i data-lucide="${field.icon}" class="w-4 h-4 text-slate-500"></i>
          ${field.label}
        </label>
        <div class="relative flex-1">
          <input type="text" id="input-${field.key}" onfocus="handleFieldFocus('${field.key}')" onblur="handleFieldBlur()" oninput="handleFieldChange('${field.key}')" class="w-full bg-slate-950/60 border border-slate-800 hover:border-slate-700 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/20 rounded-xl px-4 py-3 text-sm text-white transition outline-none">
        </div>
      </div>
      <div class="pl-4 flex-none" id="badge-container-${field.key}"></div>
    `;
    formEl.appendChild(div);
  });

  lucide.createIcons();
}

function loadCheck(checkObj) {
  activeCheckData = JSON.parse(JSON.stringify(checkObj));
  
  checkImgElement.src = currentImageSrc;
  checkImgElement.style.filter = activeCheckData.tint || "none";

  renderFormFields(activeCheckData.dokuman_tipi);

  // Bind values
  Object.keys(activeCheckData.veri).forEach(key => {
    if (key === 'tutar_uyumlu_mu') return;
    const val = activeCheckData.veri[key];
    const inputEl = document.getElementById(`input-${key}`);
    if (inputEl) {
      inputEl.value = (val === null) ? "" : val;
    }
    
    const score = activeCheckData.confidence_scores[key];
    if (score !== undefined) {
      renderBadge(key, score, val === null);
    }
  });

  // Uyuşmazlık (Tutar Uyumsuzluğu) Detection UI alerts
  const isMismatch = activeCheckData.veri.tutar_uyumlu_mu === false;
  const inputRakam = document.getElementById('input-tutar_rakam');
  const inputYazi = document.getElementById('input-tutar_yazi');

  if (isMismatch && inputRakam && inputYazi) {
    tutarAlertBox.classList.remove('hidden');
    inputRakam.classList.add('border-rose-500', 'ring-2', 'ring-rose-500/20', 'bg-rose-500/5', 'pulse-danger');
    inputYazi.classList.add('border-rose-500', 'ring-2', 'ring-rose-500/20', 'bg-rose-500/5', 'pulse-danger');
  } else {
    tutarAlertBox.classList.add('hidden');
    if (inputRakam) inputRakam.classList.remove('border-rose-500', 'ring-2', 'ring-rose-500/20', 'bg-rose-500/5', 'pulse-danger');
    if (inputYazi) inputYazi.classList.remove('border-rose-500', 'ring-2', 'ring-rose-500/20', 'bg-rose-500/5', 'pulse-danger');
  }

  // Draw coordinate frames
  drawBoundingBoxes();
  resetZoom();
}
"""

content = re.sub(r'// Binds data structure to UI fields.*?function renderBadge', load_check_replacement + "\n// Score Badges rendering\nfunction renderBadge", content, flags=re.DOTALL)


upload_replacement = """    // Map FastAPI Vision response schema to frontend presets structure
    activeCheckData = {
      dokuman_tipi: data.dokuman_tipi || "CEK",
      id: (data.veri && (data.veri.cek_no || data.veri.sozlesme_no)) || "DOC-NEW",
      bankName: (data.veri && (data.veri.banka_sube || data.veri.noterlik_adi)) || "Yeni Belge (Görsel Analiz)",
      tint: "none",
      veri: data.veri || {},
      confidence_scores: data.confidence_scores || {},
      coords: {} // We'll omit coordinates for dynamic docs
    };"""

content = re.sub(r'// Map FastAPI Vision response schema to frontend presets structure.*?coords: \{.*?\}\s*\};', upload_replacement, content, flags=re.DOTALL)

with open("static/js/app.js", "w") as f:
    f.write(content)

