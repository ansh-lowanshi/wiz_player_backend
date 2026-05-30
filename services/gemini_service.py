import google.generativeai as genai
import os
import json
import re

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)

async def get_ai_suggestions(
    song_name: str,
    artist: str | None = None
):

    prompt = f"""
You are an expert music recommendation engine.

Suggest 10 songs similar to:

Song: "{song_name}"
Artist: "{artist}"

Recommendation Rules:
- Match emotional tone closely
- Match musical vibe and energy
- Match genre and instrumentation
- Match lyrical feel
- Prefer same language
- Prefer same era/style
- Avoid repeating the same artist too much
- Avoid generic trending songs unless highly relevant
- Prefer emotionally and sonically similar tracks

IMPORTANT:
- Return REAL songs only
- Return ONLY song titles
- No artist names
- No numbering
- No explanations
- No markdown

Return ONLY valid JSON:

{{
  "songs": [
    "song name",
    "song name"
  ]
}}
"""

    response = model.generate_content(
        prompt,

        generation_config={
            "temperature": 0.5,
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 300,
        }
    )

    text = response.text.strip()

    text = re.sub(
        r"```json|```",
        "",
        text
    ).strip()

    data = json.loads(text)

    return data.get("songs", [])
