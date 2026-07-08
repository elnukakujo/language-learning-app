"""OCR pipeline: real Tesseract extraction + candidate enrichment.

Runs against actual Tesseract (no mocking) — the point is to prove the OCR
binary, pypdfium2 rendering, and the tokenize/enrich reuse all work together
end-to-end, on this machine, not just that the Python glues correctly.
"""
from PIL import Image, ImageDraw, ImageFont

from lapp.services.ocr import OcrService
from lapp.models.containers import Language

ocr_service = OcrService()


def _render_text_image(path, text):
    img = Image.new("RGB", (500, 100), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 30), text, fill="black", font=font)
    img.save(path)


def test_extract_text_from_image(tmp_path):
    image_path = tmp_path / "scan.png"
    _render_text_image(image_path, "hello world")

    text = ocr_service.extract_text(str(image_path), "eng")

    assert text.strip() == "hello world"


def test_extract_text_from_pdf(tmp_path):
    image_path = tmp_path / "page.png"
    pdf_path = tmp_path / "scan.pdf"
    _render_text_image(image_path, "bonjour le monde")
    Image.open(image_path).convert("RGB").save(pdf_path, "PDF")

    text = ocr_service.extract_text(str(pdf_path), "fra")

    assert text.strip() == "bonjour le monde"


def test_extract_candidates_enriches_words_and_characters(tmp_path):
    image_path = tmp_path / "scan.png"
    _render_text_image(image_path, "bonjour")

    language = Language(id="lang_ocr_test", user_id="user_x", name="French",
                        target_iso639_2t="fra", source_iso639_2t="eng")

    result = ocr_service.extract_candidates(str(image_path), language)

    assert "bonjour" in result["text"]
    assert result["truncated"] is False
    assert any(w["word"] == "bonjour" for w in result["words"])
    assert result["words"][0]["translation"]  # enrichment ran, not just tokenization
    assert len(result["characters"]) > 0


if __name__ == "__main__":
    print("run via: uv run pytest tests/test_ocr_service.py")
