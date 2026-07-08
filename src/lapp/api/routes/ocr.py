import logging
import uuid
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

from ...services import LanguageService, OcrService
from ...utils import MediaFileHandler

logger = logging.getLogger(__name__)

bp = Blueprint("ocr", __name__, url_prefix="/api/ocr")
language_service = LanguageService()
ocr_service = OcrService()


@bp.route("/extract", methods=["POST"])
def extract_candidates():
    """
    OCR a course scan (PDF/image) into review-ready vocabulary/character candidates.
    ---
    tags:
        - OCR
    requestBody:
        required: true
        content:
            multipart/form-data:
                schema:
                    type: object
                    properties:
                        file:
                            type: string
                            format: binary
                        language_id:
                            type: string
    responses:
        200:
            description: OCR candidates extracted (not yet inserted — client confirms before create)
        400:
            description: Bad Request - missing/invalid file, extension, or language_id
        404:
            description: Language not found
        413:
            description: File too large
        500:
            description: OCR extraction failed
    """
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    ext = Path(file.filename).suffix.lstrip(".").lower()
    allowed = current_app.config.get("ALLOWED_OCR_EXTENSIONS", {"jpg", "jpeg", "png", "pdf"})
    if ext not in allowed:
        return jsonify({"success": False, "error": f"File type not allowed. Allowed types: {allowed}"}), 400

    max_size = current_app.config.get("MAX_OCR_UPLOAD_SIZE", 20 * 1024 * 1024)
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > max_size:
        return jsonify({"success": False, "error": f"File too large. Max size: {max_size} bytes"}), 413

    language_id = request.form.get("language_id")
    if not language_id:
        return jsonify({"success": False, "error": "language_id is required"}), 400

    language = language_service.get_by_id(language_id)
    if not language:
        return jsonify({"success": False, "error": "Language not found"}), 404

    handler = MediaFileHandler(current_app.config["MEDIA_ROOT"])
    temp_path = handler.temp_root / f"ocr_{uuid.uuid4().hex}.{ext}"
    try:
        file.save(str(temp_path))
        candidates = ocr_service.extract_candidates(str(temp_path), language)
        return jsonify({"success": True, **candidates}), 200
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}", exc_info=True)
        return jsonify({"success": False, "error": "OCR extraction failed"}), 500
    finally:
        temp_path.unlink(missing_ok=True)
