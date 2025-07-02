from fastapi import UploadFile, HTTPException
import os
from datetime import datetime
import uuid
from moviepy import VideoFileClip


UPLOAD_DIR = "videos"
THUMBNAIL_DIR = "images"
ALLOWED_VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv", ".webm")


async def video_upload(file: UploadFile) -> tuple[str, str]:
    _, ext = os.path.splitext(file.filename.lower())
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(400, "Faqat video formatlar qabul qilinadi!")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex
    filename = f"{timestamp}_{unique_id}.mp4"
    video_path = os.path.join(UPLOAD_DIR, filename)

    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        clip = VideoFileClip(video_path)
        duration_video = clip.duration

        screenshot_time = 5 if duration_video > 5 else duration_video / 2
        thumbnail_filename = f"{timestamp}_{unique_id}.jpg"
        thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)

        clip.save_frame(thumbnail_path, t=screenshot_time)
        clip.close()

    except Exception as e:
        raise HTTPException(500, f"Thumbnail olishda xatolik: {e}")

    return video_path, thumbnail_path, duration_video
