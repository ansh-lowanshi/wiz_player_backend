from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.gemini_service import (
    get_ai_suggestions
)

from services.saavn_service import (
    get_song_entities
)

app = FastAPI()


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# Request Model
# =========================================

class RecommendRequest(BaseModel):
    song: str
    artist: str | None = None


# =========================================
# Routes
# =========================================

@app.get("/")
async def home():

    return {
        "success": True,
        "message": "Music Recommendation API Running"
    }


@app.post("/recommend")
async def recommend(
    body: RecommendRequest
):

    try:

        # =========================
        # Validation
        # =========================

        if len(body.song.strip()) < 3:

            return {
                "success": False,
                "message": "Song name too short",
                "data": []
            }

        print("\n============================")
        print("REQUEST RECEIVED")
        print("============================")

        print("SONG:", body.song)
        print("ARTIST:", body.artist)

        # =========================
        # Gemini Suggestions
        # =========================

        song_names = await get_ai_suggestions(
            body.song,
            body.artist
        )

        print("\nGEMINI SONGS:")
        print(song_names)

        if not song_names:

            return {
                "success": False,
                "message": "No AI recommendations found",
                "data": []
            }

        # =========================
        # Saavn Search
        # =========================

        songs = await get_song_entities(
            song_names
        )

        print("\nSAAVN RESULTS:")
        print(f"FOUND: {len(songs)} songs")

        # =========================
        # Empty Result
        # =========================

        if not songs:

            return {
                "success": False,
                "message": "No matching songs found from Saavn",
                "data": []
            }

        # =========================
        # Success
        # =========================

        return {
            "success": True,
            "total": len(songs),
            "data": songs
        }

    except Exception as e:

        print("\nERROR:")
        print(str(e))

        return {
            "success": False,
            "message": str(e),
            "data": []
        }