import httpx
import os
import asyncio

BASE_URL = os.getenv("SAAVN_BASE_URL")


async def search_song(song_name: str):

    try:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{BASE_URL}/api/search/songs",
                params={
                    "query": song_name,
                    "limit": 1
                },
                timeout=15
            )

            if response.status_code != 200:
                return None

            decoded = response.json()

            results = decoded.get(
                "data",
                {}
            ).get(
                "results",
                []
            )

            if not results:
                return None

            # Return FIRST song exactly
            return results[0]

    except Exception:
        return None


async def get_song_entities(song_names):

    tasks = [
        search_song(name)
        for name in song_names
    ]

    results = await asyncio.gather(*tasks)

    return [
        song
        for song in results
        if song is not None
    ]
