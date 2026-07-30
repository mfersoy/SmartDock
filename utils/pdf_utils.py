"""
PDF and Image Processing Utilities.
Converts uploaded PDFs/images into PIL Images and Base64 format for VLM ingestion.
"""

import io
import base64
from typing import List, Tuple
from PIL import Image

def process_file_to_images(file_bytes: bytes, file_type: str) -> List[Image.Image]:
    """
    Yüklenen dosya byte'larını PIL Image listesine çevirir.
    PDF için önce pdf2image, hata alırsa pypdfium2 dener.
    """
    images: List[Image.Image] = []

    if "pdf" in file_type.lower() or file_bytes[:4] == b'%PDF':
        # 1. Öncelik: pypdfium2 (sistem bağımlılığı gerektirmez)
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(file_bytes)
            for page in pdf:
                # 300 DPI kalitesinde render
                bitmap = page.render(scale=300 / 72)
                pil_img = bitmap.to_pil()
                images.append(pil_img)
            pdf.close()
            if images:
                return images
        except Exception:
            pass

        # 2. Öncelik: pdf2image (poppler gerektirebilir)
        try:
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(file_bytes, dpi=300)
            if images:
                return images
        except Exception as e:
            raise RuntimeError(
                f"PDF görsele dönüştürülemedi. Lütfen pypdfium2 veya pdf2image/poppler kurulu olduğundan emin olun. Hata: {str(e)}"
            )

    else:
        # PNG, JPG, JPEG vb. doğrudan Pillow ile aç
        try:
            img = Image.open(io.BytesIO(file_bytes))
            # RGB formatına çevir (RGBA veya Palette sorunlarını önlemek için)
            if img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)
        except Exception as e:
            raise ValueError(f"Görsel açılamadı: {str(e)}")

    return images


def enhance_image_for_ocr(image: Image.Image) -> Image.Image:
    """
    Soluk el yazılarını, mühürleri ve düşük kontrastlı taranmış evrakları
    VLM/OCR modellerinin en yüksek doğrulukla okuyabilmesi için iyileştirir.
    """
    from PIL import ImageEnhance, ImageFilter

    # RGB Kontrolü
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 1. Keskinleştirme (Harf kenarlarını belirginleştirir)
    enhanced = image.filter(ImageFilter.SHARPEN)

    # 2. Kontrast Artırma (%25 kontrast artışı)
    contrast_enhancer = ImageEnhance.Contrast(enhanced)
    enhanced = contrast_enhancer.enhance(1.25)

    # 3. Keskinlik Artırma
    sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
    enhanced = sharpness_enhancer.enhance(1.20)

    return enhanced


def image_to_base64(image: Image.Image, format: str = "JPEG") -> Tuple[str, str]:
    """
    PIL Image nesnesini Base64 stringine ve mime-type bilgisine dönüştürür.
    Önceden görsel iyileştirme (enhance) uygular.
    """
    # Otomatik OCR Görsel İyileştirme Uygula
    image = enhance_image_for_ocr(image)

    buffered = io.BytesIO()
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(buffered, format=format, quality=95)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    mime_type = f"image/{format.lower()}"
    return img_str, mime_type

