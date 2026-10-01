# ⚔️ OSRS Discord Bot

A feature-rich, modular Old School RuneScape (OSRS) Discord bot built with **discord.py v2.0+**. It includes live Grand Exchange price lookup, Hiscore stats and boss KC querying, combat level and drop simulation calculators, RSN availability/status checking, server GP economy management, interactive raffles, and invite tracking rewards.

---

## ✨ Key Features

- **📊 Hiscores Lookup (`/hiscores`)**
  - Fetches player skill levels, total level, overall XP, overall rank, and top 5 boss kill counts (KC) directly from official OSRS Hiscores[cite: 18].

- **⚔️ Combat Level Calculator (`/combat`)**
  - Calculates precise OSRS combat levels based on Attack, Strength, Defence, Hitpoints, Prayer, Ranged, and Magic levels.

- **🎲 Boss Drop Simulator (`/simulate_kills`)**
  - Simulates loot drops for supported bosses (e.g., Zulrah, Vorkath) up to 1,000 kills at a time.

- **📈 Grand Exchange Price Checker (`/ge`)**
  - Pulls live real-time high/low market prices and item icons directly from the official OSRS Wiki API[cite: 11].

- **🔍 RSN Status & Ban Checker (`/check_rsn`)**
  - Verifies if a RuneScape Name is active, unranked, restricted/blocked, or banned using Hiscores and RuneMetrics endpoints[cite: 14].

- **🎟 Server Raffle System (`/create_raffle`, `/draw_raffle`)**
  - Admin-created raffles with modal-based ticket purchases powered by server GP.

- **🛒 GP Reward Shop (`/shop`) & Economy**
  - Interactive dropdown menu for purchasing custom server rewards with accumulated GP.

- **🤝 Invite Tracker**
  - Automatically awards configurable server GP rewards to members when new users join via their invite links[cite: 19].

- **⚙️ Server Configuration (`/config`)**
  - Admin tools to manage GP per invite rates, shop items, and view server settings.

---

## 📁 Repository Structure

```text
├── bot.py                  # Main entry point, cog loader & command tree syncer
├── requirements.txt        # Python package dependencies
├── cogs/
│   ├── combat_calc.py      # OSRS combat level calculator
│   ├── config.py           # Admin command group for server settings & shop management
│   ├── drop_sim.py         # Boss kill drop simulator
│   ├── hiscores.py         # Player skill levels and boss kill counts lookup
│   ├── invite_tracker.py   # Automatic GP rewards on server invites
│   ├── price_check.py      # Grand Exchange live prices via Wiki API
│   ├── raffle.py           # Raffle creation and drawing system
│   ├── reward_shop.py      # Server GP reward shop interface
│   └── rsn_check.py        # RSN format validation and status checking
└── utils/
    └── db.py               # JSON/Database helper module for GP and config tracking
```

---

## 🚀 Setup & Installation

### 1. Prerequisites

* **Python 3.10+**
* A Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications).

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_optional_guild_id_for_fast_syncing

```

---

## ⚙️ Running the Bot

Start the bot using Python:

```bash
python bot.py

```

## 🛠️ Command Reference

### ⚔️ General & Player Utilities

| Command | Arguments | Description |
| --- | --- | --- |
| `/hiscores` | `<rsn>` | Look up player stats, total level, and top boss kill counts.|
| `/combat` | `<attack> <strength> <defence> <hitpoints> <prayer> [ranged] [magic]` | Calculate OSRS combat level.|
| `/simulate_kills` | `<boss> <kills>` | Simulate boss drops (Max: 1,000 kills).|
| `/ge` | `<item_name>` | View live Grand Exchange high (buy) and low (sell) prices.|
| `/check_rsn` | `<rsn>` | Check if an RSN is active, unranked, banned, or available.|


### 💰 Economy & Server Shop

| Command | Description |
| --- | --- |
| `/shop` | Open the server reward shop menu to check balance and purchase items.



### ⚙️ Admin & Management Commands

| Command | Arguments | Description |
| --- | --- | --- |
| `/create_raffle` | `<prize> <ticket_price>` | Start a new server raffle with ticket purchasing.|
| `/draw_raffle` | `<raffle_id>` | Pick a winner at random from purchased tickets.|
| `/config set_invite_reward` | `<amount>` | Set GP rewarded per successful server invite.|
| `/config add_shop_item` | `<item_name> <price>` | Add or update an item in the server shop.|
| `/config remove_shop_item` | `<item_name>` | Remove an item from the reward shop.|
| `/config view_settings` | *None* | View server invite rewards and available shop items.|

---

## 📝 License

Distributed under the MIT License.


