#!/usr/bin/env python3
"""Generate 2 additional unique room images."""
import os, base64, pathlib
from openai import OpenAI

env_path = pathlib.Path("/Users/show/Documents/kona-kon-static/.env")
for line in env_path.read_text().splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")

client = OpenAI()
OUT = pathlib.Path("/Users/show/Documents/ryokan-static/images")

JOBS = [
    ("room-mochizuki", "1536x1024",
     "Ultra-luxurious Japanese ryokan premier suite. Spacious 12-tatami main room with private "
     "outdoor hinoki cypress bath visible through open shoji on the engawa veranda. View of a deep "
     "mountain valley with autumn colors. Low table with tea set, ikebana arrangement, futon area, "
     "warm soft afternoon light. Refined wabi-sabi luxury, photo-realistic, magazine editorial. "
     "No people. No text."),
    ("room-gengetsu", "1536x1024",
     "Elegant Japanese ryokan corner deluxe guest room. 10-tatami room with a half-outdoor "
     "Shigaraki ceramic round bathtub on the balcony, east-facing window with morning light "
     "and distant mountains. Wooden ceiling beams, single hanging scroll in the tokonoma alcove, "
     "minimalist refined atmosphere. Photo-realistic, editorial. No people. No text."),
]

for slug, size, prompt in JOBS:
    out_path = OUT / f"{slug}.jpg"
    print(f"→ {slug} ...", flush=True)
    result = client.images.generate(model="gpt-image-1", prompt=prompt, size=size, quality="high", n=1)
    out_path.write_bytes(base64.b64decode(result.data[0].b64_json))
    print(f"  ✓ {out_path.stat().st_size//1024} KB")
print("Done.")
