from fastapi import FastAPI

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
from fastapi.staticfiles import StaticFiles
from utils.database import engine, Base


app = FastAPI(
    title="YouTube", openapi_url="/fastapi/loyiha/youtube/clone", docs_url="/"
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
app.include_router(user_router, tags=["User"], prefix="/user")
app.include_router(channel_router, tags=["Channel"], prefix="/channel")
app.include_router(subscription_router, tags=["Subscription"], prefix="/subscription")
app.include_router(video_router, tags=["Video"], prefix="/video")
app.include_router(like_router, tags=["Like"], prefix="/like")
app.include_router(comment_router, tags=["Comment"], prefix="/comment")
app.include_router(history_router, tags=["History"], prefix="/history")
app.include_router(playlist_router, tags=["Playlist"], prefix="/playlist")
app.include_router(
    playlist_video_router, tags=["Playlist Video"], prefix="/playlist_video"
)
app.include_router(shorts_router, tags=["Shorts"], prefix="/shorts")
app.include_router(login_router)

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
