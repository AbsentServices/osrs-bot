import json
import os

DB_FILE = "data.json"

DEFAULT_CONFIG = {
    "gp_per_invite": 100,
    "currency_name": "GP"
}

DEFAULT_SHOP = {
    "Bond": 500,
    "Abyssal Whip": 1500,
    "Dragon Dagger": 200
}

def load_db() -> dict:
    if not os.path.exists(DB_FILE):
        data = {"guilds": {}}
        save_db(data)
        return data
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data: dict) -> None:
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def ensure_guild(db: dict, guild_id: int) -> str:
    gid = str(guild_id)
    if "guilds" not in db:
        db["guilds"] = {}
    if gid not in db["guilds"]:
        db["guilds"][gid] = {
            "config": DEFAULT_CONFIG.copy(),
            "users": {},
            "shop": DEFAULT_SHOP.copy(),
            "raffles": {}
        }
    else:
        # Ensure 'config' key exists for existing guilds
        if "config" not in db["guilds"][gid]:
            db["guilds"][gid]["config"] = DEFAULT_CONFIG.copy()
    return gid

def get_guild_config(guild_id: int) -> dict:
    db = load_db()
    gid = ensure_guild(db, guild_id)
    return db["guilds"][gid]["config"]

def update_guild_config(guild_id: int, key: str, value) -> None:
    db = load_db()
    gid = ensure_guild(db, guild_id)
    db["guilds"][gid]["config"][key] = value
    save_db(db)

def get_gp(guild_id: int, user_id: int) -> int:
    db = load_db()
    gid = ensure_guild(db, guild_id)
    uid = str(user_id)
    return db["guilds"][gid]["users"].get(uid, {}).get("gp", 0)

def add_gp(guild_id: int, user_id: int, amount: int) -> None:
    db = load_db()
    gid = ensure_guild(db, guild_id)
    uid = str(user_id)
    
    users = db["guilds"][gid]["users"]
    if uid not in users:
        users[uid] = {"gp": 0, "invites": 0}
    
    users[uid]["gp"] += amount
    save_db(db)

def remove_gp(guild_id: int, user_id: int, amount: int) -> bool:
    current = get_gp(guild_id, user_id)
    if current < amount:
        return False
    add_gp(guild_id, user_id, -amount)
    return True

def get_guild_data(guild_id: int) -> dict:
    db = load_db()
    gid = ensure_guild(db, guild_id)
    save_db(db)
    return db["guilds"][gid]

def save_guild_data(guild_id: int, guild_data: dict) -> None:
    db = load_db()
    gid = ensure_guild(db, guild_id)
    db["guilds"][gid] = guild_data
    save_db(db)