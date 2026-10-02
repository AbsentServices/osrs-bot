# ⚔️ OSRS Discord Bot

An Old School RuneScape (OSRS) themed Discord bot built with `discord.py`. Features include server economy management, OSRS-themed work activities, betting games, and dedicated developer utilities.

---

## 📁 Project Structure

```text
├── main.py
├── utils/
│   └── db.py
└── cogs/
    ├── dev/
    │   ├── load.py
    │   ├── reload.py
    │   ├── sync.py
    │   └── unload.py
    ├── economy/
    │   ├── balance.py
    │   ├── daily.py
    │   ├── pay.py
    │   ├── work.py
    │   └── work_claim.py
    └── games/
        ├── alch_game.py
        ├── deaths_coffer.py
        ├── flip.py
        └── stake.py

```

---

## 📜 Command List

### 💰 Economy Commands (`cogs/economy/`)

* `/balance [user]` — Check your current GP balance or view another user's balance.
* `/pay <recipient> <amount>` — Transfer server GP to another member.
* `/daily` — Claim your daily server GP reward (24-hour cooldown).
* `/work` — Start a time-based OSRS activity (e.g., mining runite, killing Vorkath) to earn GP.
* `/work_claim` — Claim your GP reward once your active `/work` task is complete.

---

### 🎲 OSRS Betting & Games (`cogs/games/`)

* `/stake <wager>` — Stake your GP in a classic 99 HP Whip duel against the bot.
* `/alch <guess> <wager>` — High-alch an item and guess if its value is **High** (>50k GP) or **Low** (<50k GP).
* `/coffer <risk> <wager>` — Sacrifice GP to Death's Coffer with customizable risk/reward tiers:
* **Safe Sacrifice**: 70% win rate (1.35x multiplier)
* **Risky Sacrifice**: 45% win rate (2.00x multiplier)
* **Death's Gamble**: 15% win rate (5.00x multiplier)
* `/flip <choice> <wager>` — Wager GP on a 50/50 coin flip (**Heads** or **Tails**).

---


## 📜 Slayer & Skill Training (`cogs/skilling/slayer.py`)

* `/slayer task` — Get an assigned Slayer task from Masters (Turael up to Duradel) based on your level.
* `/slayer skip` — Spend earned Slayer points to skip unwanted tasks.
* `/farm plant <seed>` / `/farm harvest` — Passive farming command where players plant seeds and return hours later to harvest crops for GP rewards.

---

## 🛡️ Clue Scrolls & Minigames (`cogs/games/clues.py`)

* `/clue <tier>` — Solve a simulated Easy, Medium, Hard, Master, or Elite clue scroll step. Correct answers reward randomized casket loot (e.g., Third Age gear, Ranger Boots).
* `/barrows` — Open a Barrows chest simulator with accurate drop tables for Barrows armor pieces and runes.
* `/pet` — Roll on pet drop chances from iconic bosses (e.g., Zulrah, Vorkath, Jad) to collect rare server profile badges.

---




### 🛠️ Developer Commands (`cogs/dev/`)

*(Requires Bot Owner permissions)*

* `/sync` — Manually force-sync application slash commands with Discord.
* `/load <extension>` — Dynamically load an extension (e.g., `!load cogs.games.flip`).
* `/unload <extension>` — Dynamically unload an extension (e.g., `!unload cogs.games.flip`).
* `/reload <extension>` — Dynamically reload an extension without restarting the bot (e.g., `/reload cogs.dev.sync`).

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* Discord Bot Token & Developer Application

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/AbsentServices/osrs-bot.git](https://github.com/AbsentServices/osrs-bot.git)
cd osrs-bot

```


2. Install dependencies:
```bash
pip install -r requirements.txt

```


3. Configure your environment variables in a `.env` file at the root:
```env
DISCORD_TOKEN=your_discord_bot_token_here
GUILD_ID=your_optional_guild_id_here

```


4. Launch the bot:
```bash
python main.py

```

