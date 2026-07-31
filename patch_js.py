import re

with open("static/js/app.js", "r") as f:
    content = f.read()

# 1. Replace mockChecks entirely up to verificationHistory
new_mockChecks = """// Global Constants
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
];\n"""

content = re.sub(r'// Global Constants.*?// Seeded verification history log list', new_mockChecks + "\n// Seeded verification history log list", content, flags=re.DOTALL)


# 2. Add visual status rendering function before loadCheck
visual_status_fn = """
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
"""
content = re.sub(r'// Binds data structure to UI fields', visual_status_fn + '\n// Binds data structure to UI fields', content)

# 3. Add DOVIZ schema inside renderFormFields
schema_doviz = """  const schemaDoviz = [
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
  }"""

content = re.sub(r'  const schema = \(dokuman_tipi === "NOTER_SATIS_SOZLESMESI"\) \? schemaNoter : schemaCek;', schema_doviz, content)

# 4. Call renderVisualStatusBadges inside loadCheck
content = re.sub(r'  renderFormFields\(activeCheckData\.dokuman_tipi\);', '  renderFormFields(activeCheckData.dokuman_tipi);\n  renderVisualStatusBadges(activeCheckData.kase_var_mi, activeCheckData.imza_var_mi);', content)


# 5. Capture kase_var_mi and imza_var_mi in activeCheckData within uploadAndAnalyzeFile
upload_replacement = """    // Map FastAPI Vision response schema to frontend presets structure
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
    };"""

content = re.sub(r'    // Map FastAPI Vision response schema to frontend presets structure.*?coords: \{\} // We\'ll omit coordinates for dynamic docs\s*\};', upload_replacement, content, flags=re.DOTALL)


# 6. Update ID parsing in submitRejection/verifyAndSave
content = re.sub(r'activeCheckData\.veri\.cek_no \|\| activeCheckData\.id', 'activeCheckData.veri.cek_no || activeCheckData.veri.sozlesme_no || activeCheckData.veri.referans_no || activeCheckData.id', content)

content = re.sub(r'activeCheckData\.veri\.kesideci \|\| activeCheckData\.veri\.satici_ad_soyad \|\| "Bilinmiyor"', 'activeCheckData.veri.kesideci || activeCheckData.veri.satici_ad_soyad || activeCheckData.veri.firma_unvani || "Bilinmiyor"', content)

content = re.sub(r'activeCheckData\.veri\.tutar_rakam \|\| activeCheckData\.veri\.satis_bedeli \|\| "₺ 0,00"', 'activeCheckData.veri.tutar_rakam || activeCheckData.veri.satis_bedeli || activeCheckData.veri.tutar || "₺ 0,00"', content)


with open("static/js/app.js", "w") as f:
    f.write(content)

