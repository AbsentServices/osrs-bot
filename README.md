# ⚔️ OSRS Discord Bot

An Old School RuneScape (OSRS) themed Discord bot built with `discord.py`. Features include server economy management, OSRS-themed work activities, skilling, betting games, clue scrolls, minigames, OSRS highscores integration, Grand Exchange price tracking, clan utilities, live webhooks/feeds, an online Web Control Panel, and dedicated developer tools.

---


## 📜 Command List

### 💰 Economy Commands (`cogs/economy/`)

* `/balance [user]` — Check your current GP balance or view another user's balance.
* `/pay <recipient> <amount>` — Transfer server GP to another member.
* `/daily` — Claim your daily server GP reward (24-hour cooldown).
* `/work` — Start a time-based OSRS activity (e.g., mining runite, killing Vorkath) to earn GP.
* `/work_claim` — Claim your GP reward once your active `/work` task is complete.

Here is the updated **Skilling Commands** section formatted for your `README.md` including all 10 skilling skills and their respective subcommands:

---

### 🪓 Skilling Commands (`cogs/skilling/`)

* `/chop <tree> [quantity]` — Chop trees (Oak, Willow, Maple, Yew, Magic) to gain Woodcutting XP, gather logs for GP, and roll for the Beaver pet.
* `/cook <food> [quantity]` — Cook raw food (Shrimp, Trout, Lobster, Swordfish, Shark, Anglerfish) on a range or fire for Cooking XP and GP. Watch out for burned food!
* `/farm plant <seed>` / `/farm harvest` — Plant agricultural seeds and return later to harvest mature crops for GP rewards and Farming XP.
* `/fish <fish> [quantity]` — Cast your line for fish (Trout, Lobster, Swordfish, Monkfish, Shark, Anglerfish) to earn Fishing XP, GP, and roll for the Heron pet.
* `/mine <rock> [quantity]` — Mine ore veins (Iron, Coal, Mithril, Adamantite, Runite) to gain Mining XP, collect sellable ores, and unearth uncut gems.
* `/mix <potion> [quantity]` — Combine herbs and secondary ingredients into potions (Attack, Prayer, Super Strength, Super Restore, Saradomin Brew, Super Combat) for Herblore XP and GP.
* `/pickpocket <target> [attempts]` — Pickpocket NPCs (Man/Woman, Master Farmer, Ardougne Knight, Vyre Noble, Prifddinas Elf) for stolen GP, Thieving XP, and Rocky pet rolls. Beware of getting stunned!
* `/slayer task` — Get an assigned Slayer task from Masters (Turael up to Duradel) based on your level.
* `/slayer skip` — Spend earned Slayer points to skip unwanted tasks.
* `/smith <bar> [quantity]` — Smelt ores and smith metal bars (Bronze, Iron, Steel, Mithril, Adamantite, Rune) into gear for Smithing XP and GP.

---

### 🎲 OSRS Betting & Games (`cogs/games/`)

* `/stake <wager>` — Stake your GP in a classic 99 HP Whip duel against the bot.
* `/alch <guess> <wager>` — High-alch an item and guess if its value is **High** (>50k GP) or **Low** (<50k GP).
* `/coffer <risk> <wager>` — Sacrifice GP to Death's Coffer with customizable risk/reward tiers:
* **Safe Sacrifice**: 70% win rate (1.35x multiplier)
* **Risky Sacrifice**: 45% win rate (2.00x multiplier)
* **Death's Gamble**: 15% win rate (5.00x multiplier)


* `/flip <choice> <wager>` — Wager GP on a 50/50 coin flip (**Heads** or **Tails**).
* `/kill <monster> [quantity]` — Simulate killing a boss (e.g., Vorkath, Zulrah) $N$ times to view total loot, profit, and rare drops/pets.
* `/chest <raid> [invocation_or_points]` — Simulate opening a reward chest from Chambers of Xeric (CoX), Theatre of Blood (ToB), or Tombs of Amascut (ToA).
* `/cox_calc <party_size> <total_points>` — Calculate the team and individual unique (purple) drop rates for a CoX raid.

---

### 🛡️ Clue Scrolls & Minigames (`cogs/games/`)

* `/clue <tier>` — Solve a simulated Easy, Medium, Hard, Elite, or Master clue scroll step for randomized casket loot.
* `/barrows` — Open a Barrows chest simulator with accurate drop tables for Barrows armor pieces and runes.
* `/pet <boss>` — Roll on pet drop chances from iconic bosses (e.g., Zulrah, Vorkath, Jad, Corp) to earn rare server profile badges.

---

### ⚔️ Game Tools & Calculators (`cogs/game_tools/`)

* `/check_rsn <rsn>` — Query OSRS Hiscores and RuneMetrics APIs to check if an RSN is active, banned/blocked, or available.
* `/combat <attack> <strength> <defence> <hitpoints> <prayer> [ranged] [magic]` — Calculate precise OSRS combat level breakdowns.

---

### 🗡️ Highscores & Character Stats (`cogs/stats/hiscores.py`)

* `/hiscores <username>` — Query the official OSRS Highscores API to view level, XP, and global rank for all skills.
* `/bosses <username>` — Display boss kill counts (KC) and raid completions (ToA, CoX, ToB) for a player.
* `/gainz <username> [timeframe]` — Track skill XP gains over a daily, weekly, or monthly timeframe.

---

### 📈 Grand Exchange & Item Prices (`cogs/ge.py`)

* `/ge price <item_name>` — Fetch real-time OSRS item prices, daily volume, high/low buy limits, and price trend charts via the OSRS Wiki API.
* `/ge margin <item_name>` — View flipping margins (buy/sell spread) and potential profit per item to help users flip items in-game.

---

### 📢 Webhooks & Feeds (`cogs/notifications.py`)

* `/feed set_channel <type> #channel` — Configure dedicated channels for:
* **JMod Tweets & News**: Auto-post official game update news and blog posts.
* **OSRS Live Updates / Maintenance**: Ping when servers go down or update patches drop.
* **Clan Drop Logs**: Hook into RuneLite webhooks to stream rare clan drop notifications into Discord.



---

### 👥 Clan & Guild Features (`cogs/clan/management.py`)

* `/event create <name> <time>` — Create and schedule clan events (Raid Nights, Skill-of-the-Week, Bingo) with RSVP reaction buttons.
* `/split <total_loot> <team_size>` — Calculate raid loot splits, accounting for team size and server tax/coffer contributions.
* `/leaderboard` — Display a server-wide leaderboard showing top GP balances, duel wins, or total boss KC.

---

### 🛠️ Developer Commands (`cogs/dev/`)

*(Requires Bot Owner permissions)*

* `/sync` — Manually force-sync application slash commands with Discord.
* `/load <extension>` — Dynamically load an extension (e.g., `/load cogs.skilling.woodcutting`).
* `/unload <extension>` — Dynamically unload an extension (e.g., `/unload cogs.skilling.woodcutting`).
* `/reload <extension>` — Dynamically reload an extension without restarting the bot (e.g., `/reload cogs.dev.sync`).

---

## 🌐 Web Control Panel (`cogs/web_server.py`)

The bot includes an interactive web dashboard running on **FastAPI** (`http://localhost:8000`) that allows server admins to:

* Assign specific channels for notification feeds (JMod news, server status, clan drop webhooks).
* Toggle individual slash commands on/off per Discord server.

---



```

```

```