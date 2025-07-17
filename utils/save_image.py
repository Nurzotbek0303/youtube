from fastapi import UploadFile, HTTPException
from PIL import Image
import os
from datetime import datetime

UPLOAD_DIR = "images"


# Validatsiya funksiyasi
async def validate_image(file: UploadFile):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    max_size = 2 * 1024 * 1024  # 2 MB

    if file.content_type not in allowed_types:
        raise HTTPException(400, detail="Ruxsat etilmagan fayl turi")

    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(400, detail="Fayl hajmi juda katta (2MB dan oshmasin)")

    file.file.seek(0)


async def save_image(
    file: UploadFile, max_width: int = 1024, max_height: int = 1024, quality: int = 85
) -> str:
    await validate_image(file)

    if not file.filename.lower().endswith(
        ("png", "jpg", "jpeg", "jfif", "webp", "tiff", "gif", "svg")
    ):
        raise HTTPException(
            400, "Faqat PNG, JPG yoki JPEG formatidagi rasmlar yuklash mumkin."
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    _, file_extension = os.path.splitext(file.filename)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{timestamp}{file_extension}"
    image_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        file.file.seek(0)
        image = Image.open(file.file)

        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        image.save(image_path, format=image.format, quality=quality)

    except Exception as e:
        raise HTTPException(500, f"Rasmni saqlashda xatolik yuz berdi: {str(e)}")

    return unique_filename
