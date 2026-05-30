from fastapi import FastAPI
from pydantic import BaseModel

from services.gemini_service import (
    get_ai_suggestions
)

from services.saavn_service import (
    get_song_entities
)

app = FastAPI()


class RecommendRequest(BaseModel):
    song: str
    artist: str | None = None


@app.get("/")
async def home():
    return {
        "message": "Music Recommendation API Running"
    }


@app.post("/recommend")
async def recommend(
    body: RecommendRequest
):

    song_names = await get_ai_suggestions(
        body.song,
        body.artist
    )

    songs = await get_song_entities(
        song_names
    )

    return {
        "success": True,
        "data": songs
    }