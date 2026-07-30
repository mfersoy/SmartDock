"""
Pydantic Data Models for Turkish Official & Financial Document Analysis.
"""

from typing import Optional, Dict, Type
from pydantic import BaseModel, Field


class CekModel(BaseModel):
    """Çek Evrakı Veri Modeli"""
    keside_yeri: str = Field(
        default="Okunamadı", 
        description="Çekin düzenlendiği/kesildiği şehir veya yer"
    )
    keside_tarihi: str = Field(
        default="Okunamadı", 
        description="Çekin keşide/düzenlenme tarihi (GG/AA/YYYY formatında)"
    )
    tutar_rakam: str = Field(
        default="Okunamadı", 
        description="Çek üzerindeki rakamla tutar (örn: 50.000,00 TL)"
    )
    tutar_yazi: str = Field(
        default="Okunamadı", 
        description="Çek üzerindeki yazıyla tutar (örn: Yalnız ElliBin TürkLirası)"
    )
    hamil: str = Field(
        default="Okunamadı", 
        description="Çekin ödeneceği kişi/kurum veya lehtar/hamil adı"
    )
    kesideci_vkn_tckn: str = Field(
        default="Okunamadı", 
        description="Çeki düzenleyen keşidecinin VKN (Vergi Kimlik No) veya TCKN"
    )
    banka_bilgisi: str = Field(
        default="Okunamadı", 
        description="Banka adı ve şube bilgisi"
    )


class TapuModel(BaseModel):
    """Tapu Senedi Veri Modeli"""
    il: str = Field(
        default="Okunamadı", 
        description="Tapunun kayıtlı olduğu İl"
    )
    ilce: str = Field(
        default="Okunamadı", 
        description="Tapunun kayıtlı olduğu İlçe"
    )
    mahalle: str = Field(
        default="Okunamadı", 
        description="Mahalle / Köy adı"
    )
    ada: str = Field(
        default="Okunamadı", 
        description="Ada Numarası"
    )
    parsel: str = Field(
        default="Okunamadı", 
        description="Parsel Numarası"
    )
    nitelik: str = Field(
        default="Okunamadı", 
        description="Ana Taşınmaz Nitelik (Arsa, Daire, Tarla vb.)"
    )
    yuzolcumu: str = Field(
        default="Okunamadı", 
        description="Yüzölçümü (m² bilgisi)"
    )
    malik_adi: str = Field(
        default="Okunamadı", 
        description="Malik / Mülk Sahibi Ad-Soyad veya Unvanı"
    )
    hisse_orani: str = Field(
        default="Okunamadı", 
        description="Hisse Oranı (örn: 1/1, 1/2 vb.)"
    )


class NoterSozlesmesiModel(BaseModel):
    """Noter Araç/Gayrimenkul Sales Agreement Data Model"""
    yevmiye_no: str = Field(
        default="Okunamadı", 
        description="Noter yevmiye numarası"
    )
    tarih: str = Field(
        default="Okunamadı", 
        description="Sözleşme/İşlem tarihi"
    )
    satici_ad_soyad_unvan: str = Field(
        default="Okunamadı", 
        description="Satıcının Ad-Soyad veya Firma Unvanı"
    )
    alici_ad_soyad_unvan: str = Field(
        default="Okunamadı", 
        description="Alıcının Ad-Soyad veya Firma Unvanı"
    )
    satis_bedeli: str = Field(
        default="Okunamadı", 
        description="Sözleşmedeki satış/devir bedeli"
    )
    arac_plaka_sase_no: str = Field(
        default="Okunamadı", 
        description="Satışı yapılan araç plaka numarası veya şase numarası"
    )


class KrediTalimatiModel(BaseModel):
    """Döviz / Transfer Kredi Talimatı Veri Modeli"""
    talimat_tarihi: str = Field(
        default="Okunamadı", 
        description="Talimatın verildiği tarih"
    )
    hesap_sahibi: str = Field(
        default="Okunamadı", 
        description="Talimatı veren hesap sahibi / firma adı"
    )
    gonderilecek_tutar: str = Field(
        default="Okunamadı", 
        description="Transfer edilecek/gönderilecek tutar"
    )
    doviz_cinsi: str = Field(
        default="Okunamadı", 
        description="Döviz cinsi (TRY, USD, EUR, GBP vb.)"
    )
    alici_iban: str = Field(
        default="Okunamadı", 
        description="Alıcının IBAN numarası"
    )


# Evrak Türü Eşleme Sözlüğü
DOCUMENT_MODELS: Dict[str, Type[BaseModel]] = {
    "Çek": CekModel,
    "Tapu": TapuModel,
    "Noter Sözleşmesi": NoterSozlesmesiModel,
    "Kredi Talimatı": KrediTalimatiModel
}
