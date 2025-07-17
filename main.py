from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.user import user_router
from routers.channel import channel_router
from routers.subscription import subscription_router
from routers.video import video_router
from routers.like import like_router
from routers.comment import comment_router
from routers.history import history_router
from routers.palylist import playlist_router
from routers.playlist_video import playlist_video_router
from routers.shorts import shorts_router
from routers.auth import login_router
from routers.shorts_like import shorts_like_router
from routers.shorts_comment import shorts_commment_router
from fastapi.staticfiles import StaticFiles
from utils.database import engine, Base
import logging


app = FastAPI(
    title="YouTube", openapi_url="/fastapi/loyiha/youtube/clone", docs_url="/"
)


# Logging sozlash
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# HTTPException uchun
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail} - path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "path": request.url.path,
            },
        },
    )


# Har qanday boshqa xatolik uchun
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)} - path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "type": "InternalServerError",
                "message": "Serverda kutilmagan xatolik yuz berdi.",
                "path": request.url.path,
            },
        },
    )


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, tags=["User"])
app.include_router(channel_router, tags=["Channel"])
app.include_router(subscription_router, tags=["Subscription"])
app.include_router(video_router, tags=["Video"])
app.include_router(like_router, tags=["Like"], prefix="/like")
app.include_router(comment_router, tags=["Comment"], prefix="/comment")
app.include_router(history_router, tags=["History"], prefix="/history")
app.include_router(playlist_router, tags=["Playlist"], prefix="/playlist")
app.include_router(
    playlist_video_router, tags=["Playlist Video"], prefix="/playlist/video"
)
app.include_router(shorts_router, tags=["Shorts"], prefix="/shorts")
app.include_router(shorts_like_router, tags=["Shorts Like"], prefix="/shortsLike")
app.include_router(
    shorts_commment_router, tags=["Shorts Comment"], prefix="/shortsComment"
)
app.include_router(login_router)


app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
