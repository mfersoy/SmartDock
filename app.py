"""
Akıllı Evrak Analiz ve Otomasyon Sistemi
Streamlit UI Application
"""

import os
import io
import pandas as pd
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# Yerel modüller
from models import DOCUMENT_MODELS, CekModel, TapuModel, NoterSozlesmesiModel, KrediTalimatiModel
from utils.pdf_utils import process_file_to_images
from utils.vlm_service import analyze_document_vlm

# Env yükleme
load_dotenv()

# Streamlit Sayfa Yapılandırması
st.set_page_config(
    page_title="Akıllı Evrak Analiz Sistemi",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Stilleri
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .stCard {
        border-radius: 12px;
        padding: 1.5rem;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #DCFCE7;
        color: #166534;
        font-weight: 500;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def get_df_download_link(df: pd.DataFrame, file_type: str = "excel") -> bytes:
    """DataFrame'i Excel veya CSV byte array'e çevirir."""
    if file_type == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Evrak Verileri")
        return output.getvalue()
    else:
        return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def main():
    st.markdown('<div class="main-title">📑 Akıllı Evrak Analiz ve Otomasyon Sistemi</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Çek, Tapu, Noter Sözleşmesi ve Kredi Talimatı evraklarınızı Yapay Zeka (VLM) ile anında analiz edin ve tabloya dönüştürün.</div>', 
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------------
    # SIDEBAR: Model Yapılandırması ve API Key Girişi
    # ------------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Model ve Yapılandırma")
        
        provider = st.selectbox(
            "Yapay Zeka (VLM) Model Sağlayıcısı",
            [
                "Qwen2.5-VL-7B (Açık Kaynak SOTA #1)",
                "DeepSeek-VL2 (Açık Kaynak Vision)",
                "Meta Llama-3.2-Vision (Açık Kaynak)",
                "OpenAI (GPT-4o)",
                "Anthropic (Claude 3.5 Sonnet)",
                "Google Gemini (2.5 Flash)"
            ],
            index=0,
            help="Qwen2.5-VL, Türkçe el yazısı, silik damga ve evrak düzenlerinde şu an dünyadaki en yüksek doğruluğa sahip açık kaynak VLM modelidir."
        )

        api_key = ""
        if "Qwen" in provider or "DeepSeek" in provider or "Llama" in provider:
            st.success("🟢 Açık Kaynak Model Seçildi! Yerel Ollama (localhost:11434) veya HuggingFace API ile çalışır.")
            env_key = os.getenv("HF_TOKEN", "")
            api_key = st.text_input("HuggingFace / OpenRouter API Key (Yerel Ollama için Boş Bırakın)", value=env_key, type="password")
        elif "OpenAI" in provider:
            env_key = os.getenv("OPENAI_API_KEY", "")
            api_key = st.text_input("OpenAI API Key", value=env_key, type="password", help="sk-... ile başlayan API anahtarı")
        elif "Anthropic" in provider:
            env_key = os.getenv("ANTHROPIC_API_KEY", "")
            api_key = st.text_input("Anthropic API Key", value=env_key, type="password", help="sk-ant-... ile başlayan API anahtarı")
        else:
            env_key = os.getenv("GOOGLE_API_KEY", "")
            api_key = st.text_input("Google API Key", value=env_key, type="password", help="Gemini API anahtarı")


        st.markdown("---")
        st.header("📄 Evrak Türü Seçimi")
        doc_type = st.radio(
            "Analiz Edilecek Evrak Türü:",
            list(DOCUMENT_MODELS.keys()),
            index=0
        )

        st.info("💡 **Bilgi:** Sistem el yazısı, silik mühür ve damgalı metinleri okuyabilir.")

    # ------------------------------------------------------------------
    # ANA EKRAN: Dosya Yükleme ve Görsel Önizleme
    # ------------------------------------------------------------------
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📤 1. Evrak Yükleme")
        uploaded_file = st.file_uploader(
            "Lütfen evrak görselini veya PDF dosyasını yükleyin (Drag & Drop desteklenir):",
            type=["pdf", "png", "jpg", "jpeg"],
            help="PDF, PNG, JPG veya JPEG formatları desteklenmektedir."
        )

        images = []
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            try:
                images = process_file_to_images(file_bytes, uploaded_file.name)
                st.success(f"✅ Dosya başarıyla yüklendi! Toplam Sayfa/Görsel Sayısı: {len(images)}")
            except Exception as e:
                st.error(f"❌ Dosya okuma hatası: {str(e)}")

        if images:
            selected_page = 0
            if len(images) > 1:
                selected_page = st.slider("Analiz Edilecek Sayfa Seçimi", 1, len(images), 1) - 1
            
            st.image(
                images[selected_page], 
                caption=f"Evrak Önizleme (Sayfa {selected_page + 1}/{len(images)})", 
                use_container_width=True
            )

    # ------------------------------------------------------------------
    # ANA EKRAN: Analiz ve Tablo Gösterimi
    # ------------------------------------------------------------------
    with col2:
        st.subheader("🤖 2. Yapay Zeka Analizi ve Çıktı")

        if uploaded_file is not None and images:
            analyze_button = st.button(
                f"🚀 {doc_type} Evrakını Analiz Et", 
                type="primary", 
                use_container_width=True
            )

            if analyze_button:
                if not api_key:
                    st.warning("⚠️ Lütfen sol menüden ilgili API anahtarını girin.")
                else:
                    with st.spinner("🔍 Evrak VLM modeli ile analiz ediliyor, lütfen bekleyin..."):
                        try:
                            target_model = DOCUMENT_MODELS[doc_type]
                            img_to_analyze = images[selected_page if len(images) > 1 else 0]
                            
                            # VLM Çağrısı
                            result_model = analyze_document_vlm(
                                image=img_to_analyze,
                                model_class=target_model,
                                provider=provider,
                                api_key=api_key
                            )
                            
                            # Session State History (En son analiz edilen en üste eklenir)
                            import datetime
                            now_str = datetime.datetime.now().strftime("%H:%M:%S")
                            
                            new_entry = {
                                "Analiz Zamanı": now_str,
                                "Evrak Türü": doc_type,
                                "Dosya Adı": uploaded_file.name,
                                **result_model.model_dump()
                            }
                            
                            if "analysis_history" not in st.session_state:
                                st.session_state["analysis_history"] = []
                            
                            # En başa ekle (En son analiz edilen en üstte)
                            st.session_state["analysis_history"].insert(0, new_entry)
                            st.session_state["doc_type"] = doc_type
                            st.success("🎉 Analiz başarıyla tamamlandı ve listenin en üstüne eklendi!")
                        
                        except Exception as e:
                            st.error(f"❌ Analiz sırasında bir hata oluştu: {str(e)}")

        else:
            st.info("👈 Analize başlamak için sol taraftan bir evrak yükleyin.")

        # Kaydedilmiş Sonuç Geçmişi Tablosu ve İndirme Butonları (En son analiz edilen en üstte)
        if "analysis_history" in st.session_state and len(st.session_state["analysis_history"]) > 0:
            st.markdown("---")
            st.markdown("### 📊 Analiz Edilen Evrak Geçmişi (En Son Analiz En Üstte)")
            
            history_data = st.session_state["analysis_history"]
            df = pd.DataFrame(history_data)

            # Türkçe Okunabilir Sütun İsimleri
            column_rename_map = {
                "keside_yeri": "Keşide Yeri",
                "keside_tarihi": "Keşide Tarihi",
                "tutar_rakam": "Tutar (Rakam)",
                "tutar_yazi": "Tutar (Yazı)",
                "hamil": "Hamil",
                "kesideci_vkn_tckn": "Keşideci VKN/TCKN",
                "banka_bilgisi": "Banka Bilgisi",
                "il": "İl",
                "ilce": "İlçe",
                "mahalle": "Mahalle",
                "ada": "Ada",
                "parsel": "Parsel",
                "nitelik": "Nitelik",
                "yuzolcumu": "Yüzölçümü",
                "malik_adi": "Malik Adı",
                "hisse_orani": "Hisse Oranı",
                "yevmiye_no": "Yevmiye No",
                "tarih": "Tarih",
                "satici_ad_soyad_unvan": "Satıcı Ad-Soyad/Unvan",
                "alici_ad_soyad_unvan": "Alıcı Ad-Soyad/Unvan",
                "satis_bedeli": "Satış Bedeli",
                "arac_plaka_sase_no": "Araç Plaka/Şase No",
                "talimat_tarihi": "Talimat Tarihi",
                "hesap_sahibi": "Hesap Sahibi",
                "gonderilecek_tutar": "Gönderilecek Tutar",
                "doviz_cinsi": "Döviz Cinsi",
                "alici_iban": "Alıcı IBAN"
            }

            df = df.rename(columns=column_rename_map)

            # İnteraktif Düzenlenebilir Tablo
            edited_df = st.data_editor(
                df, 
                use_container_width=True, 
                num_rows="dynamic"
            )

            # Dışa Aktarma Butonları
            st.markdown("#### 💾 Tüm Geçmişi İndir (Export)")
            btn_col1, btn_col2 = st.columns(2)


            with btn_col1:
                excel_data = get_df_download_link(edited_df, "excel")
                st.download_button(
                    label="📥 Excel Olarak İndir (.xlsx)",
                    data=excel_data,
                    file_name=f"{doc_type.lower().replace(' ', '_')}_analiz_sonucu.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            with btn_col2:
                csv_data = get_df_download_link(edited_df, "csv")
                st.download_button(
                    label="📄 CSV Olarak İndir (.csv)",
                    data=csv_data,
                    file_name=f"{doc_type.lower().replace(' ', '_')}_analiz_sonucu.csv",
                    mime="text/csv",
                    use_container_width=True
                )


if __name__ == "__main__":
    main()
