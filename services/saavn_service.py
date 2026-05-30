import httpx
import os
import asyncio

BASE_URL = os.getenv("SAAVN_BASE_URL")


async def search_song(song_name: str):

    try:

        print("\n===================================")
        print(f"SEARCHING SONG: {song_name}")
        print("===================================")

        if not BASE_URL:

            print("ERROR: SAAVN_BASE_URL is missing")

            return None

        url = f"{BASE_URL}/api/search/songs"

        print("REQUEST URL:", url)

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                params={
                    "query": song_name,
                    "limit": 1
                },
                timeout=20
            )

            print("STATUS CODE:", response.status_code)
            print("FINAL URL:", response.url)

            if response.status_code != 200:

                print("FAILED RESPONSE:")
                print(response.text)

                return None

            decoded = response.json()

            print("RAW RESPONSE:")
            print(decoded)

            data = decoded.get("data")

            if not data:

                print("NO DATA FOUND")

                return None

            results = data.get("results", [])

            print("RESULT COUNT:", len(results))

            if not results:

                print("NO SONG RESULTS FOUND")

                return None

            first_song = results[0]

            print("FOUND SONG:")
            print(first_song.get("name"))

            return first_song

    except httpx.TimeoutException:

        print("TIMEOUT ERROR")

        return None

    except httpx.RequestError as e:

        print("REQUEST ERROR:")
        print(str(e))

        return None

    except Exception as e:

        print("UNKNOWN ERROR:")
        print(str(e))

        return None


async def get_song_entities(song_names):

    print("\n===================================")
    print("STARTING SAAVN SEARCH")
    print("===================================")

    print("TOTAL SONGS:", len(song_names))

    tasks = [
        search_song(name)
        for name in song_names
    ]

    results = await asyncio.gather(*tasks)

    valid_results = [
        song
        for song in results
        if song is not None
    ]

    print("\n===================================")
    print("FINAL RESULTS")
    print("===================================")

    print(f"SUCCESSFUL SONGS: {len(valid_results)}")

    return valid_results
