#!/usr/bin/env python3
"""Generate images via OpenAI gpt-image-1 with hybrid quality strategy.

Quality policy (per-job, matched to use case):
  - "high"   : food close-ups, faces/skin, cosmetic textures, hero product shots ($0.20/img)
  - "medium" : landscapes, gardens, architecture, interiors, abstract textures ($0.04/img)
  - "low"    : icons, thumbnails, placeholders ($0.011/img)

Add jobs as tuples: (slug, size, quality, prompt)
"""
import os, sys, base64, pathlib
from openai import OpenAI

env_path = pathlib.Path("/Users/show/Documents/kona-kon-static/.env")
for line in env_path.read_text().splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
        break

client = OpenAI()
OUT = pathlib.Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

# (slug, size, quality, prompt)
JOBS = [
    # Example — landscapes use "medium", food uses "high"
    # ("hero-rotenburo", "1536x1024", "medium", "..."),
    # ("kaiseki",        "1024x1024", "high",   "..."),
]

PRICE = {"low": 0.011, "medium": 0.04, "high": 0.20}

def main():
    if not JOBS:
        print("No JOBS defined. Edit this script's JOBS list.")
        return
    total_cost = 0.0
    for slug, size, quality, prompt in JOBS:
        out_path = OUT / f"{slug}.jpg"
        if out_path.exists():
            print(f"✓ skip {slug} (already exists)")
            continue
        cost = PRICE.get(quality, 0.20)
        total_cost += cost
        print(f"→ {slug:24s} [{quality:6s} {size:9s}]  est. ${cost:.3f}", flush=True)
        try:
            result = client.images.generate(
                model="gpt-image-1", prompt=prompt, size=size, quality=quality, n=1
            )
            out_path.write_bytes(base64.b64decode(result.data[0].b64_json))
            print(f"   ✓ saved ({out_path.stat().st_size//1024} KB)")
        except Exception as e:
            print(f"   ✗ ERROR: {e}", file=sys.stderr)
    print(f"\nDone. Estimated total: ${total_cost:.2f}")

if __name__ == "__main__":
    main()
