#!/usr/bin/env python3
"""Fetch BELIAL token price from DexTools and save as belial-data.json."""
import urllib.request, json, datetime, os

PAIR = "0xc165c9302cbab883b648d8f5f1ae13f0cc12e35e1df7e33da10a2829cfeadae9"
URL  = f"https://www.dextools.io/shared/data/pair?address={PAIR}&chain=base&audit=true&locks=false"

req = urllib.request.Request(URL, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Referer": f"https://www.dextools.io/app/base/pair-explorer/{PAIR}",
})

outdir = os.path.dirname(os.path.abspath(__file__))
path   = os.path.join(outdir, "belial-data.json")

# Load existing as fallback
existing = {}
if os.path.exists(path):
    with open(path) as f:
        existing = json.load(f)

try:
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read())

    data = d['data'][0]
    m    = data.get('metrics', {})
    ps   = data.get('periodStats', {})

    result = {
        "updated":       datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "price_usd":     data.get('price'),
        "liquidity_usd": m.get('liquidity'),
        "tx_count":      m.get('txCount'),
        "volume_24h":    ps.get('24h', {}).get('volume', {}).get('total'),
        "pair":          PAIR,
        "dex":           "flaunch",
        "source":        "dextools",
    }

    with open(path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✓ BELIAL price=${result['price_usd']:.2e} liq=${result['liquidity_usd']:,.0f} | saved")

except Exception as e:
    print(f"⚠️ DexTools fetch failed: {e} — keeping existing data")
    if not existing:
        # Write a placeholder so the page doesn't break
        with open(path, 'w') as f:
            json.dump({"updated": None, "price_usd": None, "liquidity_usd": None, "volume_24h": None, "pair": PAIR, "dex": "flaunch", "source": "dextools"}, f)
