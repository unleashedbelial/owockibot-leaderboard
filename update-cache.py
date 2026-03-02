#!/usr/bin/env python3
"""
Build agents-cache.json with all token data.
Runs via GitHub Actions every 30 minutes.
"""
import urllib.request, json, time, datetime, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents-cache.json")
AGENTS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents.json")

BELIAL_PAIR = "0xc165c9302cbab883b648d8f5f1ae13f0cc12e35e1df7e33da10a2829cfeadae9"
BELIAL_ADDR = "0x423f8663687c2f81fcac6b3696a31e36b1560d41"
BASE_RPC    = "https://gateway.tenderly.co/public/base"

BASE_ADDR = {
  "virtual-protocol":  "0x0b3e328455c4059eeb9e3f84b5543f74e24e7e1b",
  "venice-token":      "0xacfe6019ed1a7dc6f7b508c02d1b04ec88cc21bf",
  "origintrail":       "0xa81a52b4dda010896cdd386c7fbdc5cdc835ba23",
  "stp-network":       "0x1b4617734c43f6159f3a70b7e06d883647512778",
  "bankercoin-2":      "0x22af33fe49fd1fa80c7149773dde5890d3c76f3b",
  "iotex":             "0xbcbaf311cec8a4eac0430193a528d9ff27ae38c1",
  "freysa-ai":         "0xb33ff54b9f7242ef1593d2c9bcd8f9df46c77935",
  "aixbt":             "0x4f9fd6be4a90f2620860d680c0d4d5fb53d1a825",
  "magic":             "0xf1572d1da5c3cce14ee5a1c9327d17e9ff0e3f43",
  "elsa":              "0x29cc30f9d113b356ce408667aa6433589cecbdca",
  "giza":              "0x590830dfdf9a3f68afcdde2694773debdf267774",
  "paal-ai":           "0xd52333441c0553facb259600fa833a69186893a5",
  "alethea-artificial-liquid-intelligence-token": "0x97c806e7665d3afd84a8fe1837921403d59f3dcc",
  "cookie":            "0xc0041ef357b183448b235a8ea73ce4e4ec8c265f",
  "game-by-virtuals":  "0x1c4cca7c5db003824208adda61bd749e55f463a3",
  "recall":            "0x1f16e03c1a5908818f47f6ee7bb16690b40d0671",
  "cortex-2":          "0x000000000000012def132e61759048be5b5c6033",
  "wayfinder":         "0x30c7235866872213f68cb1f08c37cb9eccb93452",
  "solidus-aitech":    "0xd71552d9e08e5351adb52163b3bbbc4d7de53ce1",
  "elizaos":           "0xea17df5cf6d172224892b5477a16acb111182478",
  "morpheusai":        "0x7431ada8a591c955a994a21710752ef9b882b8e3",
  "openserv":          "0x5576d6ed9181f2225aff5282ac0ed29f755437ea",
  "autonolas":         "0x54330d28ca3357f294334bdc454a032e7f353416",
  "foom":              "0x02300ac24838570012027e0a90d3feccef3c51d2",
  "mia-2":             "0x7cea5b9548a4b48cf9551813ef9e73de916e41e0",
  "kellyclaude":       "0x50d2280441372486beecdd328c1854743ebacb07",
  "heyanon":           "0x79bbf4508b1391af3a0f4b30bb5fc4aa9ab0e07c",
  "torus":             "0x78ec15c5fd8efc5e924e9eebb9e549e29c785867",
  "mamo":              "0x7300b37dfdfab110d83290a29dfb31b1740219fe",
  "reppo":             "0xff8104251e7761163fac3211ef5583fb3f8583d6",
  "clawd-atg-eth":     "0x9f86db9fc6f7c9408e8fda3ff8ce4e78ac7a6b07",
  "theoriq":           "0x0b2558bdbc7ffec0f327fb3579c23dabd1699706",
  "genius-ai":         "0x614577036f0a024dbc1c88ba616b394dd65d105a",
  "agent-zero-token":  "0xcc4adb618253ed0d4d8a188fb901d70c54735e03",
  "felix-3":           "0xf30bf00edd0c22db54c9274b90d2a4c21fc09b07",
  "empyreal":          "0x39d5313c3750140e5042887413ba8aa6145a9bd2",
  "spectral":          "0x96419929d7949d6a801a6909c145c8eef6a40431",
  "botto":             "0x24914cb6bd01e6a0cf2a9c0478e33c25926e6a0c",
  "permission-coin":   "0xbb146326778227a8498b105a18f84e0987a684b4",
  "strawberry-ai":     "0xdf36186772a8fda4be100dbacc0b48ef00c53089",
  "1000x-by-virtuals": "0x352b850b733ab8bab50aed1dab5d22e3186ce984",
  "araistotle":        "0xfac77f01957ed1b3dd1cbea992199b8f85b6e886",
  "draiftking":        "0x7ce02e86354ea0cc3b302aeadc0ab56bc7eb44b8",
  "wasabot":           "0xc2427bf51d99b6ed0da0da103bc51235638ee868",
  "molten-3":          "0x59c0d5c34c301ac0600147924d6c9be22a2f0b07",
  "vaderai-by-virtuals":"0x731814e491571a2e9ee3c5b1f7f3b962ee8f4870",
  "moltbook":          "0xb695559b26bb2c9703ef1935c37aeae9526bab07",
  "aubrai-by-bio":     "0x9d56c29e820dd13b0580b185d0e0dc301d27581d",
  "santa-by-virtuals": "0x815269d17c10f0f3df7249370e0c1b9efe781aa8",
  "vpay":              "0x98ac5b33a4ef1151f138941c979211599c2ff953",
  "717ai-by-virtuals": "0x0b3ae50babe7ffa4e1a50569cee6bdefd4ccaee0",
  "alphakek-ai":       "0x681a09a902d9c7445b3b1ab282c38d60c72f1f09",
  "heurist":           "0xef22cb48b8483df6152e1423b19df5553bbd818b",
  "staicy-sport":      "0xd007c4c900d1df6caea2a4122f3d551d7dfe08b0",
  "maicrotrader":      "0xe74731ba9d1da6fd3c8c60ff363732bebac5273e",
  "sensay":            "0x3124678d62d2aa1f615b54525310fbfda6dcf7ae",
  "fuku-3":            "0xe10c9e9d5d8005cde4fcc5e635614665de736148",
  "axelrod-by-virtuals":"0x58db197e91bc8cf1587f75850683e4bd0730e6bf",
  "the-swarm":         "0xea87169699dabd028a78d4b91544b4298086baf6",
  "neurobro":          "0xc796e499cc8f599a2a8280825d8bda92f7a895e0",
  "jeff-ceo":          "0xa66f68ef2d8091e13585a502464bd11a159cf710",
  "sairi":             "0xde61878b0b21ce395266c44d4d548d1c72a3eb07",
  "otto-ai":           "0x380337d0180db7d0df76ac4faae2fcea908ee1fc",
  "antihunter":        "0xe2f3fae4bc62e21826018364aa30ae45d430bb07",
  "degenerate-squid":  "0x4674f73545f1db4036250ff8c33a39ad1678d864",
  "x402guard":         "0xc4047680d153fa3b741b016e871dfca723f1deea",
  "yne":               "0xe2f9db0186b13668aec9fe0e15dbd13004ed8d6f",
  "gloria-ai":         "0x3b313f5615bbd6b200c71f84ec2f677b94df8674",
  "perkos":            "0xf714e60f85497d70508f7e356b5db80e64539ba3",
  "faircaster":        "0x7d928816cc9c462dd7adef911de41535e444cb07",
  "luna-by-virtuals":  "0x55cd6469f597452b5a7536e2cd98fde4c1247ee4",
  "ribbita-by-virtuals":"0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00",
}

SOCIAL = {
  "virtual-protocol": {"website":"https://virtuals.io",    "twitter":"https://x.com/virtuals_io"},
  "aixbt":            {"website":"https://aixbt.com",       "twitter":"https://x.com/aixbt_agent"},
  "kellyclaude":      {"twitter":"https://x.com/KellyClaudeAI"},
  "game-by-virtuals": {"website":"https://vvaifu.fun",      "twitter":"https://x.com/gamefivirtuals"},
  "elizaos":          {"website":"https://elizaos.ai",      "twitter":"https://x.com/elizaos"},
  "autonolas":        {"website":"https://olas.network",    "twitter":"https://x.com/autonolas"},
  "recall":           {"website":"https://recall.network",  "twitter":"https://x.com/recallnet"},
  "freysa-ai":        {"website":"https://freysa.ai",       "twitter":"https://x.com/0xFreysa"},
  "morpheusai":       {"website":"https://mor.org",         "twitter":"https://x.com/MorpheusAIs"},
  "wayfinder":        {"website":"https://wayfinder.xyz",   "twitter":"https://x.com/Wayfinder_AI"},
  "heyanon":          {"website":"https://heyanon.xyz",     "twitter":"https://x.com/hey_anon_ai"},
  "spectral":         {"website":"https://spectral.finance","twitter":"https://x.com/spectralfinance"},
  "venice-token":     {"website":"https://venice.ai",       "twitter":"https://x.com/venice_ai"},
  "cortex-2":         {"website":"https://cortex.io",       "twitter":"https://x.com/CortexAI"},
}

def get_json(url, headers=None, timeout=15):
    hdrs = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    if headers: hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def fetch_cg(page):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=ai-agents&order=market_cap_desc&per_page=100&page={page}&sparkline=true&price_change_percentage=24h"
    return get_json(url)

def fetch_dex_batch(addresses):
    """Batch DexScreener, return {addr: best_base_pair}"""
    result = {}
    for chunk in chunks(addresses, 28):
        try:
            d = get_json(f"https://api.dexscreener.com/latest/dex/tokens/{','.join(chunk)}")
            for p in [p for p in (d.get("pairs") or []) if p.get("chainId") == "base"]:
                addr = p["baseToken"]["address"].lower()
                cur_liq = result.get(addr, {}).get("liquidity", {}).get("usd", 0) or 0
                new_liq = (p.get("liquidity") or {}).get("usd", 0) or 0
                if new_liq >= cur_liq:
                    result[addr] = p
        except Exception as e:
            print(f"  DexScreener chunk failed: {e}")
        time.sleep(0.5)
    return result

def fetch_dextools_belial():
    """Fetch BELIAL data from DexTools (server-side works with right headers)."""
    url = f"https://www.dextools.io/shared/data/pair?address={BELIAL_PAIR}&chain=base&audit=true&locks=false"
    d = get_json(url, headers={
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Referer": f"https://www.dextools.io/app/base/pair-explorer/{BELIAL_PAIR}",
    })
    data = d["data"][0]
    m    = data.get("metrics", {})
    ps   = data.get("periodStats", {})
    ps24 = ps.get("24h", {})
    ps7d = ps.get("7d", {})
    return {
        "price_usd":        data.get("price"),
        "liquidity_usd":    m.get("liquidity"),
        "tx_count":         m.get("txCount"),
        "reserve":          m.get("reserve"),          # token reserve in pool
        "volume_24h":       (ps24.get("volume") or {}).get("total"),
        "volume_7d":        (ps7d.get("volume") or {}).get("total"),
        "price_change_24h": ps24.get("priceVariation"),
        "buys_24h":         ps24.get("buys"),
        "sells_24h":        ps24.get("sells"),
    }

def fetch_total_supply(token_address):
    """eth_call totalSupply() on Base."""
    payload = json.dumps({
        "jsonrpc":"2.0","method":"eth_call",
        "params":[{"to": token_address, "data": "0x18160ddd"}, "latest"],
        "id": 1
    }).encode()
    req = urllib.request.Request(BASE_RPC, data=payload, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read())
    hex_val = d.get("result","0x0")
    return int(hex_val, 16)

def main():
    print(f"[{datetime.datetime.now(datetime.timezone.utc).isoformat()}] Building agents-cache.json...")

    agents = []
    seen   = set()  # addresses already added

    # ── 1. CoinGecko ai-agents (pages 1+2) ─────────────────────────────────
    print("  Fetching CoinGecko pages 1+2...")
    cg_coins = []
    for page in [1, 2]:
        try:
            data = fetch_cg(page)
            cg_coins.extend(data)
            print(f"    Page {page}: {len(data)} coins")
        except Exception as e:
            print(f"    Page {page} failed: {e}")
        time.sleep(1.2)

    # Match CG coins to Base addresses
    cg_agents = []
    for coin in cg_coins:
        addr = BASE_ADDR.get(coin["id"])
        if not addr or addr.lower() in seen:
            continue
        seen.add(addr.lower())
        social = SOCIAL.get(coin["id"], {})
        cg_agents.append({
            "id":           coin["id"],
            "name":         coin["name"],
            "symbol":       coin["symbol"].upper(),
            "address":      addr,
            "image":        coin.get("image"),
            "market_cap":   coin.get("market_cap"),
            "volume_24h":   coin.get("total_volume"),
            "price":        coin.get("current_price"),
            "change_24h":   coin.get("price_change_percentage_24h"),
            "sparkline":    coin.get("sparkline_in_7d", {}).get("price") or [],
            "source":       "cg",
            "dex":          None,
            "dex_url":      None,
            "website":      social.get("website",""),
            "twitter":      social.get("twitter",""),
            "chart":        None,
        })
    print(f"  {len(cg_agents)} CG agents matched to Base addresses")

    # ── 2. Enrich CG agents with DexScreener (dex label + chart link) ──────
    print("  Enriching CG agents with DexScreener...")
    cg_addrs = [a["address"] for a in cg_agents]
    dex_map  = fetch_dex_batch(cg_addrs)
    for ag in cg_agents:
        pair = dex_map.get(ag["address"].lower())
        if pair:
            ag["dex"]     = pair.get("dexId")
            ag["dex_url"] = pair.get("url")
            # DexScreener price/mcap can be more accurate - use if significantly different
            ds_price = float(pair.get("priceUsd") or 0)
            ds_mcap  = pair.get("marketCap") or pair.get("fdv")
            if ds_price and not ag["price"]:
                ag["price"]      = ds_price
                ag["market_cap"] = ds_mcap
            # Auto-image from DexScreener if CG image is a thumb
            if pair.get("info", {}).get("imageUrl"):
                ag["_dex_image"] = pair["info"]["imageUrl"].split("?")[0]
        else:
            ag["dex"] = "coingecko"   # No Base pair found → mark source
        agents.append(ag)

    # ── 3. Manual tokens from agents.json ───────────────────────────────────
    print("  Loading agents.json manual tokens...")
    try:
        with open(AGENTS_JSON) as f:
            manual_list = json.load(f).get("agents", [])
    except Exception as e:
        print(f"  agents.json load failed: {e}")
        manual_list = []

    manual_addrs = [t["address"] for t in manual_list if t["address"].lower() not in seen]
    if manual_addrs:
        print(f"  Fetching {len(manual_addrs)} manual tokens from DexScreener...")
        manual_dex = fetch_dex_batch(manual_addrs)
    else:
        manual_dex = {}

    for t in manual_list:
        addr_lower = t["address"].lower()
        if addr_lower in seen:
            continue
        seen.add(addr_lower)

        # Special: BELIAL via DexTools
        if addr_lower == BELIAL_ADDR.lower():
            print("  Fetching BELIAL from DexTools...")
            try:
                dt  = fetch_dextools_belial()
                # Get total supply for mcap
                try:
                    supply = fetch_total_supply(t["address"])
                    supply_f = supply / 1e18
                    mcap   = supply_f * dt["price_usd"] if dt.get("price_usd") else None
                    print(f"    BELIAL: price=${dt['price_usd']:.2e} supply={supply_f:.2e} mcap=${mcap:.0f}")
                except Exception as e:
                    print(f"    totalSupply failed: {e}")
                    mcap = None

                agents.append({
                    "id":         "belial",
                    "name":       t.get("name","Belial"),
                    "symbol":     t.get("symbol","BELIAL"),
                    "address":    t["address"],
                    "image":      t.get("image","images/belial.svg"),
                    "market_cap": mcap,
                    "volume_24h": dt.get("volume_24h"),
                    "price":      dt.get("price_usd"),
                    "change_24h": dt.get("price_change_24h"),
                    "liquidity":  dt.get("liquidity_usd"),
                    "sparkline":  [],
                    "source":     "dextools",
                    "dex":        "flaunch",
                    "dex_url":    t.get("chart",""),
                    "website":    t.get("website",""),
                    "twitter":    t.get("twitter",""),
                    "chart":      t.get("chart",""),
                    "tx_count":   dt.get("tx_count"),
                })
            except Exception as e:
                print(f"    DexTools BELIAL failed: {e}")
            continue

        # Other manual tokens via DexScreener
        pair = manual_dex.get(addr_lower)
        agents.append({
            "id":         addr_lower,
            "name":       t.get("name", addr_lower[:8]),
            "symbol":     t.get("symbol","???"),
            "address":    t["address"],
            "image":      t.get("image") or (pair["info"]["imageUrl"].split("?")[0] if pair and pair.get("info",{}).get("imageUrl") else None),
            "market_cap": pair.get("marketCap") or pair.get("fdv") if pair else None,
            "volume_24h": pair["volume"]["h24"] if pair and pair.get("volume") else None,
            "price":      float(pair["priceUsd"]) if pair and pair.get("priceUsd") else None,
            "change_24h": pair["priceChange"]["h24"] if pair and pair.get("priceChange") else None,
            "liquidity":  pair["liquidity"]["usd"] if pair and pair.get("liquidity") else None,
            "sparkline":  [],
            "source":     "dex" if pair else "manual",
            "dex":        pair["dexId"] if pair else ("flaunch" if t.get("chart") else "lowliq"),
            "dex_url":    pair.get("url","") if pair else t.get("chart",""),
            "website":    t.get("website","") or (pair["info"]["websites"][0]["url"] if pair and pair.get("info",{}).get("websites") else ""),
            "twitter":    t.get("twitter","") or "",
            "chart":      t.get("chart",""),
        })

    # ── 4. Save ─────────────────────────────────────────────────────────────
    out = {
        "updated":  datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "count":    len(agents),
        "agents":   agents,
    }

    # Only write if data is non-trivially different (protect against partial failures)
    if len(agents) < 10:
        print(f"⚠️  Only {len(agents)} agents — suspiciously low, keeping existing cache")
        return

    # Fallback: keep existing entries for tokens that failed this run
    existing = {}
    if os.path.exists(OUT):
        try:
            with open(OUT) as f:
                old = json.load(f)
            for a in old.get("agents",[]):
                existing[a["address"].lower()] = a
        except: pass

    for ag in agents:
        addr = ag["address"].lower()
        old = existing.get(addr, {})
        # If price is None but we had one before, keep old price
        if ag.get("price") is None and old.get("price") is not None:
            ag["price"] = old["price"]
        if ag.get("market_cap") is None and old.get("market_cap") is not None:
            ag["market_cap"] = old["market_cap"]

    with open(OUT, "w") as f:
        json.dump(out, f, separators=(",",":"))

    print(f"✓ Saved {len(agents)} agents to agents-cache.json")
    dex_counts = {}
    for a in agents:
        dex_counts[a.get("dex","null")] = dex_counts.get(a.get("dex","null"),0)+1
    for k,v in sorted(dex_counts.items(), key=lambda x:-x[1]):
        print(f"   {k}: {v}")

if __name__ == "__main__":
    main()
