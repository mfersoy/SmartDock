// Global Constants
const CONFIDENCE_THRESHOLD = 80;

// Default bank check presets matching mock data scenarios
const mockChecks = [
  {
    id: "CHK-1001",
    dokuman_tipi: "CEK",
    bankName: "First United Bank",
    tint: "none",
    kase_var_mi: true,
    imza_var_mi: true,
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
      cek_no: 98, banka_sube: 95, kesideci: 92, keside_tarihi: 85, tutar_rakam: 99, tutar_yazi: 88,
      kase_var_mi: 95, imza_var_mi: 99
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
    kase_var_mi: true,
    imza_var_mi: true,
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
      satici_ad_soyad: 90, alici_ad_soyad: 95, vekil_ad_soyad: 0,
      kase_var_mi: 98, imza_var_mi: 95
    },
    coords: {}
  },
  {
    id: "CHK-45829",
    dokuman_tipi: "CEK",
    bankName: "Garanti BBVA",
    tint: "hue-rotate(110deg) saturate(1.1)",
    kase_var_mi: false,
    imza_var_mi: true,
    veri: {
      cek_no: "4582910",
      banka_sube: null,
      kesideci: "ASYA TEKSTİL SAN. VE TİC. LTD. ŞTİ.",
      keside_tarihi: "2026-07-30",
      tutar_rakam: "₺ 150.000,00",
      tutar_yazi: "YüzElliBin TürkLirası",
      tutar_uyumlu_mu: true
    },
    confidence_scores: {
      cek_no: 97, banka_sube: 0, kesideci: 91, keside_tarihi: 89, tutar_rakam: 99, tutar_yazi: 74,
      kase_var_mi: 90, imza_var_mi: 85
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
    kase_var_mi: true,
    imza_var_mi: false,
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
      cek_no: 96, banka_sube: 82, kesideci: 94, keside_tarihi: 76, tutar_rakam: 98, tutar_yazi: 60,
      kase_var_mi: 88, imza_var_mi: 82
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
    id: "DVT-9012",
    dokuman_tipi: "DOVIZ_KREDISI_TALIMATI",
    bankName: "Akbank T.A.Ş.",
    tint: "grayscale(20%) sepia(10%)",
    kase_var_mi: true,
    imza_var_mi: true,
    veri: {
      banka_adi: "Akbank T.A.Ş.",
      sube_adi: "Beşiktaş Şubesi",
      iban_hesap_no: "TR12 0006 2000 0001 2345 6789 01",
      referans_no: "8829103",
      talimat_tarihi: "2026-08-01",
      tutar: "15.000,00",
      para_birimi: "USD",
      firma_unvani: "GÜNEŞ İTHALAT İHRACAT A.Ş.",
      vergi_dairesi_vkn: "Zincirlikuyu VD - 1234567890",
      ticaret_sicil_no: "654321-0"
    },
    confidence_scores: {
      banka_adi: 99, sube_adi: 95, iban_hesap_no: 98, referans_no: 92,
      talimat_tarihi: 97, tutar: 99, para_birimi: 99, firma_unvani: 95,
      vergi_dairesi_vkn: 88, ticaret_sicil_no: 90,
      kase_var_mi: 96, imza_var_mi: 98
    },
    coords: {}
  }
];

// Seeded verification history log list
let verificationHistory = [
  { id: "CHK-90212", bank: "T. İş Bankası", client: "ZİRVETEK BİLİŞİM A.Ş.", amount: "₺ 89.200,00", status: "Doğrulandı", match: "Uyumlu", time: "11:20:14" },
  { id: "CHK-76123", bank: "Akbank", client: "NURİ ALÇO DIŞ TİC.", amount: "₺ 12.500,00", status: "Reddedildi", match: "Uyumlu", time: "10:45:09", note: "İmza Eksikliği / Geçersiz İmza" },
  { id: "CHK-33421", bank: "QNB Finansbank", client: "DERYA LOJİSTİK LTD.", amount: "₺ 270.000,00", status: "Doğrulandı", match: "Uyumlu", time: "09:30:55" }
];

// App State Variables
let currentPresetIndex = 0;
let activeCheckData = null;
let customUploadedFile = null;
let currentImageSrc = "/static/assets/sample_check.png";
let autoFocusEnabled = true;

// Zoom/Pan workspace variables
let scale = 1.0;
let panX = 0;
let panY = 0;
let isDragging = false;
let startX, startY;

// DOM View References
let viewerContainer, zoomableWrapper, checkImgElement, bboxesContainer;
let scannerOverlay, scannerLine, scanningLabel, tutarAlertBox;

window.addEventListener('DOMContentLoaded', () => {
  // Bind references
  viewerContainer = document.getElementById('viewer-container');
  zoomableWrapper = document.getElementById('zoomable-wrapper');
  checkImgElement = document.getElementById('check-image');
  bboxesContainer = document.getElementById('bounding-boxes-container');
  scannerOverlay = document.getElementById('scanner-overlay');
  scannerLine = document.getElementById('scanner-line');
  scanningLabel = document.getElementById('scanning-label');
  tutarAlertBox = document.getElementById('tutar-alert-container');

  // Load Icons
  lucide.createIcons();
  
  // Render default check
  loadCheck(mockChecks[0]);
  
  // Render log database
  renderHistoryTable();

  // Mouse pan drag events
  viewerContainer.addEventListener('pointerdown', (e) => {
    if (e.button !== 0) return;
    isDragging = true;
    startX = e.clientX - panX;
    startY = e.clientY - panY;
    viewerContainer.style.cursor = 'grabbing';
    viewerContainer.setPointerCapture(e.pointerId);
  });

  viewerContainer.addEventListener('pointermove', (e) => {
    if (!isDragging) return;
    panX = e.clientX - startX;
    panY = e.clientY - startY;
    updateTransform();
  });

  viewerContainer.addEventListener('pointerup', (e) => {
    isDragging = false;
    viewerContainer.style.cursor = 'grab';
    viewerContainer.releasePointerCapture(e.pointerId);
  });

  viewerContainer.addEventListener('pointercancel', () => {
    isDragging = false;
    viewerContainer.style.cursor = 'grab';
  });

  // Wheel Zoom events
  viewerContainer.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = 1.1;
    const oldScale = scale;
    
    if (e.deltaY < 0) {
      scale = Math.min(scale * zoomFactor, 6.0);
    } else {
      scale = Math.max(scale / zoomFactor, 0.4);
    }
    
    const rect = viewerContainer.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    panX = mouseX - (mouseX - panX) * (scale / oldScale);
    panY = mouseY - (mouseY - panY) * (scale / oldScale);
    
    updateTransform();
  }, { passive: false });
});

function updateTransform() {
  zoomableWrapper.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
}

function zoomIn() {
  scale = Math.min(scale * 1.25, 6.0);
  updateTransform();
}

function zoomOut() {
  scale = Math.max(scale / 1.25, 0.4);
  updateTransform();
}

function resetZoom() {
  scale = 1.0;
  panX = 0;
  panY = 0;
  updateTransform();
}

function toggleAutoFocus() {
  autoFocusEnabled = !autoFocusEnabled;
  const toggle = document.getElementById('auto-focus-toggle');
  const dot = document.getElementById('auto-focus-toggle-dot');
  if (autoFocusEnabled) {
    toggle.classList.remove('bg-slate-700');
    toggle.classList.add('bg-indigo-600');
    dot.classList.remove('translate-x-0');
    dot.classList.add('translate-x-4');
    showToast("Otomatik Odaklama Aktif", "info");
  } else {
    toggle.classList.remove('bg-indigo-600');
    toggle.classList.add('bg-slate-700');
    dot.classList.remove('translate-x-4');
    dot.classList.add('translate-x-0');
    showToast("Otomatik Odaklama Devre Dışı", "info");
  }
}

// Vision AI Info settings modal toggles
function openPromptModal() {
  const modal = document.getElementById('prompt-guide-modal');
  const inner = modal.querySelector('div');
  modal.classList.remove('pointer-events-none', 'opacity-0');
  inner.classList.remove('scale-95');
  inner.classList.add('scale-100');
}

function closePromptModal() {
  const modal = document.getElementById('prompt-guide-modal');
  const inner = modal.querySelector('div');
  modal.classList.add('pointer-events-none', 'opacity-0');
  inner.classList.remove('scale-100');
  inner.classList.add('scale-95');
}

function switchModalTab(tabName) {
  const promptBtn = document.getElementById('tab-btn-prompt');
  const schemaBtn = document.getElementById('tab-btn-schema');
  const promptContent = document.getElementById('tab-content-prompt');
  const schemaContent = document.getElementById('tab-content-schema');

  if (tabName === 'prompt') {
    promptBtn.className = "px-4 py-2 text-xs font-semibold text-white border-b-2 border-indigo-500";
    schemaBtn.className = "px-4 py-2 text-xs font-semibold text-slate-400 hover:text-slate-200 border-b-2 border-transparent";
    promptContent.classList.remove('hidden');
    schemaContent.classList.add('hidden');
  } else {
    schemaBtn.className = "px-4 py-2 text-xs font-semibold text-white border-b-2 border-indigo-500";
    promptBtn.className = "px-4 py-2 text-xs font-semibold text-slate-400 hover:text-slate-200 border-b-2 border-transparent";
    schemaContent.classList.remove('hidden');
    promptContent.classList.add('hidden');
  }
}

// Dynamic Preset Selector dropdown
function selectCheckPreset(index) {
  currentPresetIndex = index;
  customUploadedFile = null;
  currentImageSrc = "/static/assets/sample_check.png";
  loadCheck(mockChecks[index]);
  showToast(`${mockChecks[index].bankName} Evrağı Yüklendi`, "info");
}


function renderVisualStatusBadges(kase, imza) {
  const container = document.getElementById('visual-status-container');
  if (!container) return;
  
  if (kase === undefined && imza === undefined) {
    container.classList.add('hidden');
    container.innerHTML = '';
    return;
  }
  
  container.classList.remove('hidden');
  
  const kaseHtml = kase === true 
    ? `<div class="flex items-center space-x-2 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg text-sm font-semibold">
         <i data-lucide="check-circle" class="w-4 h-4"></i>
         <span>Kaşe Mevcut</span>
       </div>`
    : `<div class="flex items-center space-x-2 px-3 py-1.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-lg text-sm font-semibold pulse-danger">
         <i data-lucide="x-circle" class="w-4 h-4"></i>
         <span>Kaşe Eksik</span>
       </div>`;
       
  const imzaHtml = imza === true 
    ? `<div class="flex items-center space-x-2 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg text-sm font-semibold">
         <i data-lucide="check-circle" class="w-4 h-4"></i>
         <span>İmza Mevcut</span>
       </div>`
    : `<div class="flex items-center space-x-2 px-3 py-1.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-lg text-sm font-semibold pulse-danger">
         <i data-lucide="x-circle" class="w-4 h-4"></i>
         <span>İmza Eksik</span>
       </div>`;

  container.innerHTML = kaseHtml + imzaHtml;
  lucide.createIcons();
}

// Binds data structure to UI fields
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

  const schemaDoviz = [
    { key: 'banka_adi', label: 'Banka Adı', icon: 'landmark' },
    { key: 'sube_adi', label: 'Şube Adı', icon: 'building' },
    { key: 'iban_hesap_no', label: 'IBAN / Hesap No', icon: 'credit-card' },
    { key: 'referans_no', label: 'Referans No', icon: 'hash' },
    { key: 'talimat_tarihi', label: 'Talimat Tarihi', icon: 'calendar' },
    { key: 'tutar', label: 'Tutar', icon: 'circle-dollar-sign' },
    { key: 'para_birimi', label: 'Para Birimi', icon: 'coins' },
    { key: 'firma_unvani', label: 'Firma Ünvanı', icon: 'briefcase' },
    { key: 'vergi_dairesi_vkn', label: 'Vergi Dairesi ve VKN', icon: 'file-text' },
    { key: 'ticaret_sicil_no', label: 'Ticaret Sicil No', icon: 'hash' }
  ];

  let schema = schemaCek;
  if (dokuman_tipi === "NOTER_SATIS_SOZLESMESI") {
    schema = schemaNoter;
  } else if (dokuman_tipi === "DOVIZ_KREDISI_TALIMATI") {
    schema = schemaDoviz;
  }

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
  renderVisualStatusBadges(activeCheckData.kase_var_mi, activeCheckData.imza_var_mi);

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

// Score Badges rendering
function renderBadge(key, score, isNull = false, isModified = false) {
  const container = document.getElementById(`badge-container-${key}`);
  if (!container) return;

  const inputEl = document.getElementById(`input-${key}`);

  if (isNull) {
    container.innerHTML = `
      <div class="inline-flex items-center space-x-1 px-2.5 py-1 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-lg text-xs font-semibold select-none pulse-danger">
        <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-ping"></span>
        <span>%0 (Okunamadı)</span>
      </div>
    `;
    if (inputEl) {
      inputEl.classList.remove('border-slate-800', 'focus:border-indigo-500');
      inputEl.classList.add('border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20');
    }
  } else if (isModified) {
    container.innerHTML = `
      <div class="inline-flex items-center space-x-1 px-2.5 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-lg text-xs font-semibold select-none">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
        <span>Manuel</span>
      </div>
    `;
    if (inputEl) {
      inputEl.classList.remove('border-rose-900/80', 'border-rose-500', 'ring-2', 'ring-rose-500/20', 'bg-rose-500/5', 'pulse-danger');
      inputEl.classList.remove('border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
      inputEl.classList.add('border-slate-800', 'focus:border-indigo-500');
    }
  } else {
    const isGood = score >= 80;
    const isWarning = score > 0 && score < 80;
    
    let colorClass, iconClass, textClass;
    
    if (isGood) {
      colorClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
      iconClass = 'bg-emerald-400';
    } else if (isWarning) {
      colorClass = 'bg-orange-500/10 text-orange-400 border-orange-500/20';
      iconClass = 'bg-orange-400';
    } else {
      colorClass = 'bg-rose-500/10 text-rose-400 border-rose-500/20 pulse-danger';
      iconClass = 'bg-rose-500 animate-ping';
    }
    
    container.innerHTML = `
      <div class="inline-flex items-center space-x-1 px-2.5 py-1 ${colorClass} border rounded-lg text-xs font-semibold select-none">
        <span class="w-1.5 h-1.5 rounded-full ${iconClass}"></span>
        <span>%${score}</span>
      </div>
    `;

    if (inputEl) {
      if (isGood) {
        inputEl.classList.remove('border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20', 'border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
        inputEl.classList.add('border-slate-800', 'focus:border-indigo-500');
      } else if (isWarning) {
        inputEl.classList.remove('border-slate-800', 'focus:border-indigo-500', 'border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20');
        inputEl.classList.add('border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
      } else {
        inputEl.classList.remove('border-slate-800', 'focus:border-indigo-500', 'border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
        inputEl.classList.add('border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20');
      }
    }
  }
}

// User inputs values
function handleFieldChange(key) {
  if (!activeCheckData) return;
  const inputEl = document.getElementById(`input-${key}`);
  if (!inputEl) return;
  
  activeCheckData.veri[key] = inputEl.value;

  // If tutar is modified, clear mismatch visuals
  if (key === 'tutar_rakam' || key === 'tutar_yazi') {
    tutarAlertBox.classList.add('hidden');
    inputEl.classList.remove('border-rose-500', 'ring-2', 'ring-rose-500/20', 'bg-rose-500/5');
  }

  renderBadge(key, 100, false, true);
}

// Visual bounding boxes coordinates highlights
function drawBoundingBoxes() {
  bboxesContainer.innerHTML = '';
  if (!activeCheckData) return;

  Object.keys(activeCheckData.coords).forEach(key => {
    const coord = activeCheckData.coords[key];
    const score = activeCheckData.confidence_scores[key];
    const val = activeCheckData.veri[key];

    const box = document.createElement('div');
    box.id = `bbox-${key}`;
    box.className = `absolute border border-dashed border-indigo-400/40 bg-indigo-500/5 rounded hover:border-emerald-400 hover:bg-emerald-500/10 cursor-pointer pointer-events-auto transition-all duration-200`;
    box.style.left = `${coord.left}%`;
    box.style.top = `${coord.top}%`;
    box.style.width = `${coord.width}%`;
    box.style.height = `${coord.height}%`;
    
    box.setAttribute('title', `${getFieldNameTR(key)} (Güven: %${val === null ? 0 : score})`);
    
    box.addEventListener('click', () => {
      const inputEl = document.getElementById(`input-${key}`);
      if (inputEl) {
        inputEl.focus();
        inputEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });

    bboxesContainer.appendChild(box);
  });
}

function handleFieldFocus(key) {
  if (!activeCheckData) return;
  
  const boxes = bboxesContainer.querySelectorAll('div');
  boxes.forEach(box => {
    box.className = `absolute border border-dashed border-indigo-400/40 bg-indigo-500/5 rounded hover:border-emerald-400 hover:bg-emerald-500/10 cursor-pointer pointer-events-auto transition-all duration-200`;
  });

  const activeBox = document.getElementById(`bbox-${key}`);
  if (activeBox) {
    activeBox.className = `absolute border-2 border-emerald-400 bg-emerald-500/10 rounded cursor-pointer pointer-events-auto shadow-lg shadow-emerald-500/20 ring-4 ring-emerald-500/20 z-10 transition-all duration-200`;
  }

  if (autoFocusEnabled) {
    const coord = activeCheckData.coords[key];
    zoomToField(coord.left, coord.top, coord.width, coord.height);
  }
}

function handleFieldBlur() {
  setTimeout(() => {
    const hasFocused = document.activeElement && document.activeElement.id.startsWith('input-');
    if (!hasFocused) {
      const boxes = bboxesContainer.querySelectorAll('div');
      boxes.forEach(box => {
        box.className = `absolute border border-dashed border-indigo-400/40 bg-indigo-500/5 rounded hover:border-emerald-400 hover:bg-emerald-500/10 cursor-pointer pointer-events-auto transition-all duration-200`;
      });
    }
  }, 100);
}

function zoomToField(leftPercent, topPercent, widthPercent, heightPercent) {
  const containerWidth = viewerContainer.clientWidth;
  const containerHeight = viewerContainer.clientHeight;
  
  const targetXPercent = leftPercent + widthPercent / 2;
  const targetYPercent = topPercent + heightPercent / 2;
  
  scale = 2.0;
  
  const wrapperWidth = zoomableWrapper.clientWidth;
  const wrapperHeight = zoomableWrapper.clientHeight;
  
  const rawTargetX = (targetXPercent / 100) * wrapperWidth;
  const rawTargetY = (targetYPercent / 100) * wrapperHeight;
  
  panX = (containerWidth / 2) - rawTargetX * scale;
  panY = (containerHeight / 2) - rawTargetY * scale;
  
  updateTransform();
}

// OCR scanner visual effect trigger
function runScanAnimation() {
  scannerOverlay.classList.add('scanning');
  scannerLine.classList.add('scanning');
  
  const actionButtons = document.querySelectorAll('main button');
  actionButtons.forEach(btn => btn.disabled = true);
  
  showToast("OCR Optik Evrak Taraması Başladı...", "info");

  setTimeout(() => {
    scannerOverlay.classList.remove('scanning');
    scannerLine.classList.remove('scanning');
    actionButtons.forEach(btn => btn.disabled = false);

    // If custom image loaded, re-analyze it from service
    if (customUploadedFile) {
      uploadAndAnalyzeFile(customUploadedFile);
    } else {
      // Reload preset values
      loadCheck(mockChecks[currentPresetIndex]);
      showToast("Tarama tamamlandı. Veriler güncellendi.", "success");
    }
  }, 2000);
}

// FastAPI File Upload handler
async function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  customUploadedFile = file;

  // 1. Locally preview file in container
  const reader = new FileReader();
  reader.onload = function(e) {
    currentImageSrc = e.target.result;
    checkImgElement.src = currentImageSrc;
    checkImgElement.style.filter = "none";
  };
  reader.readAsDataURL(file);

  // 2. Send image payload to FastAPI
  await uploadAndAnalyzeFile(file);
}

// Upload & fetch handler
async function uploadAndAnalyzeFile(fileObj) {
  // Show spinner overlay inside viewer
  scanningLabel.classList.remove('hidden');
  scanningLabel.classList.add('flex');
  tutarAlertBox.classList.add('hidden');

  const formData = new FormData();
  formData.append('file', fileObj);

  try {
    const response = await fetch('/api/analyze-check', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`HTTP Error status: ${response.status}`);
    }

    const data = await response.json();

        // Map FastAPI Vision response schema to frontend presets structure
    activeCheckData = {
      dokuman_tipi: data.dokuman_tipi || "CEK",
      kase_var_mi: data.kase_var_mi,
      imza_var_mi: data.imza_var_mi,
      id: (data.veri && (data.veri.cek_no || data.veri.sozlesme_no || data.veri.referans_no)) || "DOC-NEW",
      bankName: (data.veri && (data.veri.banka_sube || data.veri.noterlik_adi || data.veri.banka_adi)) || "Yeni Belge (Görsel Analiz)",
      tint: "none",
      veri: data.veri || {},
      confidence_scores: data.confidence_scores || {},
      coords: {} // We'll omit coordinates for dynamic docs
    };

    if (data.is_mock) {
      showToast("Vision API bağlantı hatası: Sunucu tarafı simülasyonu devrede.", "warning");
    } else {
      showToast("Vision AI ile çek görseli başarıyla analiz edildi!", "success");
    }

    loadCheck(activeCheckData);

  } catch (err) {
    console.error("API error:", err);
    showToast("API sunucusuyla iletişim kurulamadı.", "warning");
  } finally {
    scanningLabel.classList.remove('flex');
    scanningLabel.classList.add('hidden');
  }
}

// Rejections modals controls
function openRejectModal() {
  const modal = document.getElementById('reject-modal');
  const inner = modal.querySelector('div');
  modal.classList.remove('pointer-events-none', 'opacity-0');
  inner.classList.remove('scale-95');
  inner.classList.add('scale-100');
}

function closeRejectModal() {
  const modal = document.getElementById('reject-modal');
  const inner = modal.querySelector('div');
  modal.classList.add('pointer-events-none', 'opacity-0');
  inner.classList.remove('scale-100');
  inner.classList.add('scale-95');
  document.getElementById('reject-notes').value = '';
}

function submitRejection() {
  const reason = document.querySelector('input[name="reject-reason"]:checked').value;
  const note = document.getElementById('reject-notes').value.trim();
  const combinedReason = note ? `${reason} (${note})` : reason;

  const newEntry = {
    id: activeCheckData.veri.cek_no || activeCheckData.veri.sozlesme_no || activeCheckData.veri.referans_no || activeCheckData.id,
    bank: activeCheckData.bankName,
    client: activeCheckData.veri.kesideci || activeCheckData.veri.satici_ad_soyad || activeCheckData.veri.firma_unvani || "Bilinmiyor",
    amount: activeCheckData.veri.tutar_rakam || activeCheckData.veri.satis_bedeli || activeCheckData.veri.tutar || "₺ 0,00",
    status: "Reddedildi",
    match: (activeCheckData.veri.tutar_uyumlu_mu ?? true) ? "Uyumlu" : "Uyuşmazlık",
    time: getCurrentTimeString(),
    note: combinedReason
  };

  verificationHistory.unshift(newEntry);
  
  incrementStat('stat-rejected');
  incrementStat('stat-processed');
  recalculateAverageAccuracy();

  showToast(`Evrak REDDEDİLDİ: ${reason}`, "warning");
  renderHistoryTable();
  closeRejectModal();

  cycleNextDocument();
}

function verifyAndSave() {
  const isMismatch = (activeCheckData.veri.tutar_uyumlu_mu ?? true) === false;

  const newEntry = {
    id: activeCheckData.veri.cek_no || activeCheckData.veri.sozlesme_no || activeCheckData.veri.referans_no || activeCheckData.id,
    bank: activeCheckData.bankName,
    client: activeCheckData.veri.kesideci || activeCheckData.veri.satici_ad_soyad || activeCheckData.veri.firma_unvani || "Bilinmiyor",
    amount: activeCheckData.veri.tutar_rakam || activeCheckData.veri.satis_bedeli || activeCheckData.veri.tutar || "₺ 0,00",
    status: "Doğrulandı",
    match: isMismatch ? "Uyuşmazlık" : "Uyumlu",
    time: getCurrentTimeString()
  };

  verificationHistory.unshift(newEntry);
  
  incrementStat('stat-verified');
  incrementStat('stat-processed');
  recalculateAverageAccuracy();

  showToast("Evrak Doğrulandı ve Kaydedildi", "success");
  renderHistoryTable();

  cycleNextDocument();
}

function cycleNextDocument() {
  customUploadedFile = null;
  currentImageSrc = "/static/assets/sample_check.png";
  
  currentPresetIndex = (currentPresetIndex + 1) % mockChecks.length;
  document.getElementById('check-selector').value = currentPresetIndex;
  
  setTimeout(() => {
    loadCheck(mockChecks[currentPresetIndex]);
    runScanAnimation();
  }, 600);
}

// Calculations & Utilities
function calculateAverageScore(check) {
  if (!check) return 0;
  let total = 0;
  let count = 0;
  Object.keys(check.confidence_scores).forEach(key => {
    total += check.confidence_scores[key];
    count++;
  });
  return Math.round(total / count);
}

function recalculateAverageAccuracy() {
  let sum = 0;
  const count = mockChecks.length;
  mockChecks.forEach(c => {
    sum += calculateAverageScore(c);
  });
  const avg = (sum / count).toFixed(1);
  document.getElementById('stat-accuracy').innerText = `%${avg}`;
}

function incrementStat(elementId) {
  const el = document.getElementById(elementId);
  if (el) {
    let val = parseInt(el.innerText);
    el.innerText = val + 1;
  }
}

function getCurrentTimeString() {
  const now = new Date();
  return now.toTimeString().split(' ')[0];
}

function getFieldNameTR(key) {
  const trNames = {
    cek_no: "Çek Numarası",
    banka_sube: "Banka ve Şube",
    kesideci: "Keşideci",
    keside_tarihi: "Keşide Tarihi",
    tutar_rakam: "Rakamla Tutar",
    tutar_yazi: "Yazıyla Tutar"
  };
  return trNames[key] || key;
}

// Render history table UI
function renderHistoryTable() {
  const tbody = document.getElementById('history-table-body');
  if (!tbody) return;
  tbody.innerHTML = '';

  verificationHistory.forEach(row => {
    const isVerified = row.status === "Doğrulandı";
    const statusBadge = isVerified 
      ? `<span class="inline-flex items-center space-x-1 px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-md font-semibold text-[10px]">
          <i data-lucide="check" class="w-3 h-3"></i>
          <span>Onaylandı</span>
         </span>`
      : `<span class="inline-flex items-center space-x-1 px-2 py-0.5 bg-rose-500/10 border border-rose-500/30 text-rose-400 rounded-md font-semibold text-[10px]" title="${row.note || ''}">
          <i data-lucide="x" class="w-3 h-3"></i>
          <span>Reddedildi</span>
         </span>`;

    const isCompliant = row.match === "Uyumlu";
    const complianceBadge = isCompliant
      ? `<span class="inline-flex items-center space-x-1 px-1.5 py-0.5 bg-slate-800 text-slate-400 rounded-md text-[10px]">
          <span>Uyumlu</span>
         </span>`
      : `<span class="inline-flex items-center space-x-1 px-1.5 py-0.5 bg-rose-500/15 border border-rose-500/20 text-rose-400 rounded-md text-[10px] font-semibold animate-pulse">
          <i data-lucide="alert-triangle" class="w-2.5 h-2.5"></i>
          <span>Tutar Farkı</span>
         </span>`;

    const tr = document.createElement('tr');
    tr.className = "hover:bg-slate-900/30 border-b border-slate-800/40 transition duration-100";
    tr.innerHTML = `
      <td class="py-3 px-5 font-mono text-slate-300 font-semibold">${row.id}</td>
      <td class="py-3 px-5 text-slate-300">${row.bank}</td>
      <td class="py-3 px-5 text-slate-300 truncate max-w-[200px]" title="${row.client}">${row.client}</td>
      <td class="py-3 px-5 font-mono text-slate-300">${row.amount}</td>
      <td class="py-3 px-5">${complianceBadge}</td>
      <td class="py-3 px-5">${statusBadge}</td>
      <td class="py-3 px-5 text-right font-mono text-slate-400">${row.time}</td>
    `;
    tbody.appendChild(tr);
  });

  document.getElementById('session-count').innerText = `Bu oturumda ${verificationHistory.length} kayıt işlendi`;
  lucide.createIcons();
}

// Toast rendering alert
function showToast(message, type = "success") {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  
  let icon = 'check-circle';
  let iconColor = 'text-emerald-400';
  let bgBorder = 'bg-slate-900/90 border-emerald-500/30 text-slate-200';
  
  if (type === "warning") {
    icon = 'alert-triangle';
    iconColor = 'text-rose-400';
    bgBorder = 'bg-slate-900/90 border-rose-500/30 text-slate-200';
  } else if (type === "info") {
    icon = 'info';
    iconColor = 'text-indigo-400';
    bgBorder = 'bg-slate-900/90 border-indigo-500/30 text-slate-200';
  }

  toast.className = `flex items-center space-x-3 px-4.5 py-3 border rounded-xl shadow-2xl backdrop-blur-md transition-all duration-300 transform translate-y-4 opacity-0 pointer-events-auto ${bgBorder}`;
  toast.innerHTML = `
    <i data-lucide="${icon}" class="w-5 h-5 ${iconColor}"></i>
    <span class="text-xs font-semibold">${message}</span>
  `;
  
  container.appendChild(toast);
  lucide.createIcons();

  setTimeout(() => {
    toast.classList.remove('translate-y-4', 'opacity-0');
  }, 50);

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3500);
}
