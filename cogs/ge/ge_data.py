import aiohttp

# Required by OSRS Wiki API guidelines: custom User-Agent header
HEADERS = {
    "User-Agent": "OSRSDiscordBot/1.0 (Contact: admin@example.com)"
}

# In-memory item cache: {item_name_lower: item_id}
_item_mapping_cache = {}


async def get_item_mapping() -> dict:
    """Fetch and cache the full OSRS Wiki item mapping (name to ID)."""
    global _item_mapping_cache
    if _item_mapping_cache:
        return _item_mapping_cache

    url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data:
                    _item_mapping_cache[item["name"].lower()] = {
                        "id": item["id"],
                        "name": item["name"],
                        "limit": item.get("limit", "N/A"),
                        "highalch": item.get("highalch", 0)
                    }
    return _item_mapping_cache


async def fetch_latest_price(item_id: int) -> dict | None:
    """Fetch latest high and low price for a given item ID."""
    url = f"https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("data", {}).get(str(item_id))
    return None