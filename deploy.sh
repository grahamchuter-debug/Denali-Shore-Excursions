#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -f node_modules/.bin/wrangler ]]; then npm install; fi
echo "Deploying Denali Shore Excursions to Cloudflare..."
npx wrangler deploy
echo "Done. Check https://denalishoreexcursions.com/ shortly."
