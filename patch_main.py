import re
import random

with open("app/main.py", "r") as f:
    content = f.read()

fallback_logic = """        # Generate robust mock fallback to maintain visual workflow interactivity
        doc_type = random.choice(["CEK", "NOTER_SATIS_SOZLESMESI", "DOVIZ_KREDISI_TALIMATI"])
        is_compliant = random.random() > 0.35
        has_null = random.random() > 0.8
        has_kase = random.choice([True, False])
        has_imza = random.choice([True, False])
        
        fallback_data = {
            "dokuman_tipi": doc_type,
            "kase_var_mi": has_kase,
            "imza_var_mi": has_imza,
            "is_mock": True,
            "error_msg": str(e),
            "veri": {},
            "confidence_scores": {
                "kase_var_mi": random.randint(85, 99),
                "imza_var_mi": random.randint(85, 99)
            }
        }
        
        if doc_type == "CEK":
            fallback_data["veri"] = {
                "cek_no": str(random.randint(110200, 998900)),
                "banka_sube": None if has_null else "Türkiye İş Bankası - Maslak Ticari Şubesi (Fallback)",
                "kesideci": "FALLBACK MOCK DIŞ TİC. LTD. ŞTİ.",
                "keside_tarihi": "2026-07-31",
                "tutar_rakam": "₺ 92.400,00",
                "tutar_yazi": "DoksanİkiBinDörtYüz TürkLirası" if is_compliant else "DoksanBin TürkLirası",
                "tutar_uyumlu_mu": is_compliant
            }
            fallback_data["confidence_scores"].update({
                "cek_no": random.randint(85, 99),
                "banka_sube": 0 if has_null else random.randint(75, 95),
                "kesideci": random.randint(80, 98),
                "keside_tarihi": random.randint(82, 97),
                "tutar_rakam": random.randint(88, 99),
                "tutar_yazi": random.randint(60, 94)
            })
        elif doc_type == "NOTER_SATIS_SOZLESMESI":
            fallback_data["veri"] = {
                "noterlik_adi": None if has_null else "İstanbul 14. Noterliği",
                "sozlesme_no": str(random.randint(10000, 99999)),
                "islem_tarihi": "2026-07-31",
                "plaka_no": "34 ABC 123",
                "marka_model": "Volkswagen Golf",
                "sasi_no": "WVGZZZ123456789",
                "motor_no": "CJZ123456",
                "satis_bedeli": "₺ 850.000,00",
                "satici_ad_soyad": "AHMET YILMAZ",
                "alici_ad_soyad": "MEHMET KAYA",
                "vekil_ad_soyad": None
            }
            fallback_data["confidence_scores"].update({
                "noterlik_adi": 0 if has_null else random.randint(85, 99),
                "sozlesme_no": random.randint(85, 99),
                "islem_tarihi": random.randint(85, 99),
                "plaka_no": random.randint(85, 99),
                "marka_model": random.randint(85, 99),
                "sasi_no": random.randint(85, 99),
                "motor_no": random.randint(85, 99),
                "satis_bedeli": random.randint(85, 99),
                "satici_ad_soyad": random.randint(85, 99),
                "alici_ad_soyad": random.randint(85, 99),
                "vekil_ad_soyad": 0
            })
        else:
            # DOVIZ_KREDISI_TALIMATI
            fallback_data["veri"] = {
                "banka_adi": "Akbank T.A.Ş.",
                "sube_adi": "Beşiktaş Şubesi",
                "iban_hesap_no": "TR12 0006 2000 0001 2345 6789 01",
                "referans_no": str(random.randint(500000, 999999)),
                "talimat_tarihi": "2026-08-01",
                "tutar": "15.000,00",
                "para_birimi": "USD",
                "firma_unvani": "GÜNEŞ İTHALAT İHRACAT A.Ş.",
                "vergi_dairesi_vkn": "Zincirlikuyu VD - 1234567890",
                "ticaret_sicil_no": "654321-0"
            }
            fallback_data["confidence_scores"].update({
                "banka_adi": random.randint(85, 99),
                "sube_adi": random.randint(85, 99),
                "iban_hesap_no": random.randint(85, 99),
                "referans_no": random.randint(85, 99),
                "talimat_tarihi": random.randint(85, 99),
                "tutar": random.randint(85, 99),
                "para_birimi": random.randint(85, 99),
                "firma_unvani": random.randint(85, 99),
                "vergi_dairesi_vkn": random.randint(85, 99),
                "ticaret_sicil_no": random.randint(85, 99)
            })

        return JSONResponse(content=fallback_data)"""

content = re.sub(r'# Generate robust mock fallback.*return JSONResponse\(content=fallback_data\)', fallback_logic, content, flags=re.DOTALL)

with open("app/main.py", "w") as f:
    f.write(content)

