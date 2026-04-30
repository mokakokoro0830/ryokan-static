#!/bin/bash
# Generate 4 seasonal ryokan garden images via OpenAI API (curl, no SDK).
set -e

API_KEY=$(grep '^OPENAI_API_KEY=' /Users/show/Documents/kona-kon-static/.env | cut -d= -f2 | tr -d '"' | tr -d "'")
OUT="/Users/show/Documents/ryokan-static/images"
mkdir -p "$OUT"

BASE="Traditional Japanese ryokan garden, photographed from a low angle. Stone lantern (toro) on the left, koi pond reflecting the scene, moss-covered stones, raked white gravel, traditional wooden ryokan veranda visible in the background, shoji screens. Editorial photography, magazine quality, soft natural light, shallow depth of field, photorealistic. No people. No text. No signs."

declare -a SLUGS=("season-spring" "season-summer" "season-autumn" "season-winter")
declare -a EXTRAS=(
  "SPRING SCENE: pale pink wild cherry blossoms (yamazakura) in soft bloom, petals scattered on the moss and water surface, gentle morning light, pastel atmosphere, subtle pink and green tones."
  "SUMMER SCENE: deep verdant green moss and maple leaves, lush bamboo grove behind, golden afternoon sun filtering through trees, dragonflies near the pond, rich saturated greens, vibrant lush atmosphere."
  "AUTUMN SCENE: brilliant red and orange Japanese maple leaves (momiji) in full color, crimson leaves floating on the pond surface, fallen leaves on the moss, warm golden afternoon light, rich autumn color palette of red, orange, amber."
  "WINTER SCENE: pristine white snow blanket on stone lantern and pine branches, snow-covered moss, bare maple branches, frozen pond surface, soft cold blue light, minimalist serene atmosphere, muted blue-white palette."
)

for i in "${!SLUGS[@]}"; do
  SLUG="${SLUGS[$i]}"
  PROMPT="$BASE ${EXTRAS[$i]}"
  echo "→ $SLUG"

  PAYLOAD=$(jq -n --arg p "$PROMPT" '{model:"gpt-image-1", prompt:$p, size:"1536x1024", quality:"medium", n:1}')

  RESPONSE=$(curl -sS https://api.openai.com/v1/images/generations \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

  # Check error
  ERR=$(echo "$RESPONSE" | jq -r '.error.message // empty')
  if [ -n "$ERR" ]; then
    echo "  ✗ ERROR: $ERR"
    exit 1
  fi

  echo "$RESPONSE" | jq -r '.data[0].b64_json' | base64 -d > "$OUT/$SLUG.jpg"
  SIZE=$(stat -f%z "$OUT/$SLUG.jpg")
  echo "  ✓ saved ($((SIZE/1024)) KB)"
done

echo "Done."
