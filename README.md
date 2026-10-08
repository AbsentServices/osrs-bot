# ⚔️ OSRS Discord Bot

An Old School RuneScape (OSRS) themed Discord bot built with `discord.py`. Features include server economy management, OSRS-themed work activities, betting games, and dedicated developer utilities.

---

## 📁 Project Structure

```text
Coming Soon1!
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
* `/clue <tier>` — Solve a simulated Easy, Medium, Hard, Master, or Elite clue scroll step. Correct answers reward randomized casket loot (e.g., Third Age gear, Ranger Boots).
* `/barrows` — Open a Barrows chest simulator with accurate drop tables for Barrows armor pieces and runes.
* `/pet` — Roll on pet drop chances from iconic bosses (e.g., Zulrah, Vorkath, Jad) to collect rare server profile badges.

---


## 📜 Skill Training (`cogs/skilling/`)


### Slayer (`cogs/skilling/slayer.py`)
* `/slayer task` — Get an assigned Slayer task from Masters (Turael up to Duradel) based on your level.
* `/slayer skip` — Spend earned Slayer points to skip unwanted tasks.


---

## 🛡️ Clue Scrolls & Minigames (`cogs/games/`)

* `/clue <tier>` — Solve a simulated Easy, Medium, Hard, Master, or Elite clue scroll step. Correct answers reward randomized casket loot (e.g., Third Age gear, Ranger Boots).
* `/barrows` — Open a Barrows chest simulator with accurate drop tables for Barrows armor pieces and runes.
* `/pet` — Roll on pet drop chances from iconic bosses (e.g., Zulrah, Vorkath, Jad) to collect rare server profile badges.

---

## 🗡️ Highscores & Character Stats (`cogs/stats/hiscores.py`)

* `/hiscores <username>` — Query the official OSRS Highscores API to view level, XP, and global rank for all skills.
* `/bosses <username>` — Display boss kill counts (KC) and raid completions (ToA, CoX, ToB) for a player.
* `/gainz <username> [timeframe]` — Track skill XP gains over a daily, weekly, or monthly timeframe.

---

## 📈 Grand Exchange & Item Prices (`cogs/ge.py`)

* `/ge price <item_name>` — Fetch real-time OSRS item prices, daily volume, high/low buy limits, and price trend charts via the OSRS Wiki API.
* `/ge margin <item_name>` — View flipping margins (buy/sell spread) and potential profit per item to help users flip items in-game.

---

## 👥 Clan & Guild Features (`cogs/clan/management.py`)

* `/event create <name> <time>` — Create and schedule clan events (Raid Nights, Skill-of-the-Week, Bingo) with RSVP reaction buttons.
* `/split <total_loot> <team_size>` — Calculate raid loot splits, accounting for team size and server tax/coffer contributions.
* `/leaderboard` — Display a server-wide leaderboard showing the top GP balances, duel wins, or total boss KC.
---

### 📢 Webhooks & Live Feeds (`cogs/notifications.py`)

* `/feed set_channel <type> #channel` — Configure dedicated announcement channels for automated feeds:
  * **JMod Tweets & News**: Auto-post game updates and official OSRS news blogs.
  * **OSRS Live Updates / Maintenance**: Alert when servers undergo scheduled updates or maintenance.
  * **Clan Drop Logs**: Hook into RuneLite webhooks to stream rare drop announcements into Discord in real-time.

---

### 🗡️ Monster & Boss Drop Simulators (`cogs/games/pvm.py`)

* `/kill <monster> [quantity]` — Simulate killing a boss (e.g., Vorkath, Zulrah) $N$ times and view total loot collected, profit earned, and rare drops/pets obtained.
* `/chest <raid> [invocation_or_points]` — Simulate opening a reward chest from Chambers of Xeric (CoX), Theatre of Blood (ToB), or Tombs of Amascut (ToA).
* `/cox_calc <party_size> <total_points>` — Calculate the exact team and individual unique drop probabilities for a CoX raid.


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

