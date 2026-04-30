#!/usr/bin/env python3
"""Generate 4 seasonal ryokan garden images. Quality: medium (landscapes)."""
import os, base64, pathlib, sys
from openai import OpenAI

env_path = pathlib.Path("/Users/show/Documents/kona-kon-static/.env")
for line in env_path.read_text().splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")

client = OpenAI()
OUT = pathlib.Path("/Users/show/Documents/ryokan-static/images")

BASE = (
    "Traditional Japanese ryokan garden, photographed from a low angle. "
    "Stone lantern (toro) on the left, koi pond reflecting the scene, "
    "moss-covered stones, raked white gravel, traditional wooden ryokan veranda visible in the background, "
    "shoji screens. Editorial photography, magazine quality, soft natural light, "
    "shallow depth of field, photorealistic. No people. No text. No signs."
)

JOBS = [
    ("season-spring", "1536x1024", "medium",
     BASE + " SPRING SCENE: pale pink wild cherry blossoms (yamazakura) in soft bloom, "
     "petals scattered on the moss and water surface, gentle morning light, pastel atmosphere, "
     "subtle pink and green tones."),
    ("season-summer", "1536x1024", "medium",
     BASE + " SUMMER SCENE: deep verdant green moss and maple leaves, lush bamboo grove behind, "
     "golden afternoon sun filtering through trees, dragonflies near the pond, "
     "rich saturated greens, vibrant lush atmosphere."),
    ("season-autumn", "1536x1024", "medium",
     BASE + " AUTUMN SCENE: brilliant red and orange Japanese maple leaves (momiji) in full color, "
     "crimson leaves floating on the pond surface, fallen leaves on the moss, "
     "warm golden afternoon light, rich autumn color palette of red, orange, amber."),
    ("season-winter", "1536x1024", "medium",
     BASE + " WINTER SCENE: pristine white snow blanket on stone lantern and pine branches, "
     "snow-covered moss, bare maple branches, frozen pond surface, soft cold blue light, "
     "minimalist serene atmosphere, muted blue-white palette."),
]

PRICE = {"low": 0.011, "medium": 0.04, "high": 0.20}

total = 0
for slug, size, quality, prompt in JOBS:
    out = OUT / f"{slug}.jpg"
    cost = PRICE[quality]
    total += cost
    print(f"→ {slug:20s} [{quality:6s} {size}]  est. ${cost:.3f}", flush=True)
    try:
        r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size, quality=quality, n=1)
        out.write_bytes(base64.b64decode(r.data[0].b64_json))
        print(f"   ✓ {out.stat().st_size//1024} KB")
    except Exception as e:
        print(f"   ✗ {e}", file=sys.stderr)
        sys.exit(1)
print(f"\nDone. Total: ${total:.2f}")
