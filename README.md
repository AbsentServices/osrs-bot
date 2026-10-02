# ⚔️ OSRS Discord Bot

A feature-rich, modular Old School RuneScape (OSRS) Discord bot built with **discord.py v2.0+**. It includes live Grand Exchange price lookup, Hiscore stats and boss KC querying, combat level and drop simulation calculators, RSN status checking, server GP economy management, interactive raffles, clan events, bingo, and invite tracking rewards.

---

## ✨ Key Features

- **📊 Hiscores & Price Checks (`/hiscores`, `/ge`)**
  - Fetches player skill levels, total level, overall XP, overall rank, top boss kill counts (KC), and live Grand Exchange prices.

- **⚔️ Game Tools & Calculators (`/slayer_task`, `/dryness`, `/xp_calc`, `/quest_reqs`)**
  - Slayer task info, drop dryness binomial calculators, target XP action calculators, and quest requirements checking.

- **🏆 Clan Events & Competitions (`/event_create`, `/event_list`, `/sotw`, `/botw`, `/bingo`)**
  - Interactive RSVP event posts, Skill/Boss of the Week leaderboards, and clan bingo submission tracking.

- **💰 Economy & Server Shop (`/shop`, `/balance`, `/pay`, `/daily`)**
  - Server GP economy with peer-to-peer transfers, daily rewards, raffles, and item reward shop.

- **🛡️ Admin & Economy Management (`/config ...`)**
  - Admin controls to manage GP balances, reset economy, set invite rewards, and manage shop listings.

---

## 📁 Repository Structure

```text
├── bot.py                     # Main entry point, cog loader & command tree syncer
├── requirements.txt           # Python package dependencies
├── cogs/
│   ├── admin/
│   │   └── eco/
│   │       ├── add_gp.py       # Manually award GP to a member
│   │       ├── remove_gp.py    # Deduct GP from a member
│   │       └── reset_economy.py# Reset server GP balances
│   ├── clan_events/
│   │   ├── bingo.py           # Clan bingo board & submission tracker
│   │   ├── botw.py            # Boss of the Week leaderboard
│   │   ├── event_create.py    # Schedule clan event with RSVP buttons
│   │   ├── event_list.py      # List active clan events
│   │   └── sotw.py            # Skill of the Week leaderboard
│   ├── game_tools/
│   │   ├── dryness.py         # Statistical dryness calculator
│   │   ├── quest_reqs.py      # Quest stat requirement checker
│   │   ├── slayer_task.py     # Slayer task lookup & recommendations
│   │   └── xp_calc.py         # XP & action calculator
│   ├── unity/
│   │   ├── add_shop_item.py   # Add item to reward shop
│   │   ├── invite_tracker.py  # Automatic GP rewards on server invites
│   │   ├── remove_shop_item.py# Remove item from reward shop
│   │   ├── set_invite_reward.py# Configure GP per invite rate
│   │   └── view_settings.py   # View server settings & shop
│   ├── combat_calc.py         # OSRS combat level calculator
│   ├── drop_sim.py            # Boss kill drop simulator
│   ├── hiscores.py            # Player stats lookup
│   ├── price_check.py         # Grand Exchange live prices
│   ├── raffle.py              # Raffle creation and drawing system
│   ├── reward_shop.py         # Server GP reward shop interface
│   └── rsn_check.py           # RSN format validation and status check
└── utils/
    └── db.py                  # Database/JSON helper module

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

---

## 🛠️️ Command Reference

### ⚔️ General & Player Utilities

| Command | Arguments | Description |
| --- | --- | --- |
| `/hiscores` | `<rsn>` | Look up player stats, total level, and top boss kill counts. |
| `/combat` | `<attack> <strength> <defence> <hitpoints> <prayer> [ranged] [magic]` | Calculate OSRS combat level. |
| `/simulate_kills` | `<boss> <kills>` | Simulate boss drops (Max: 1,000 kills). |
| `/ge` | `<item_name>` | View live Grand Exchange high/low prices. |
| `/check_rsn` | `<rsn>` | Check if an RSN is active, unranked, banned, or available. |

---

### 🎮 Game Tools & Calculators (`cogs/game_tools/`)

| Command | Arguments | Description |
| --- | --- | --- |
| `/slayer_task` | `<task_name>` | Slayer task weakness, locations, and gear recommendations. |
| `/dryness` | `<kc> <drop_rate>` | Binomial probability dryness/luck calculator. |
| `/xp_calc` | `<current_xp> <target_level> <xp_per_action>` | Calculate actions required to reach target level. |
| `/quest_reqs` | `<quest_name>` | Check player stat requirements for major quests. |

---

### 🏆 Clan & Activity Features (`cogs/clan_events/`)

| Command | Arguments | Description |
| --- | --- | --- |
| `/event_create` | `<title> <description> <time>` | Schedule a clan event with RSVP buttons (DPS, Tank, Healer, Learner). |
| `/event_list` | *None* | View active scheduled clan events. |
| `/sotw` | `<skill>` | Skill of the Week leaderboard tracking XP gains. |
| `/botw` | `<boss>` | Boss of the Week leaderboard tracking kill counts. |
| `/bingo` | `[tile] [proof]` | Clan bingo board status and tile screenshot submission. |

---

### 💰 Economy & Gambling Features (Server GP)

| Command | Arguments | Description |
| --- | --- | --- |
| `/shop` | *None* | Interactive server shop menu to purchase custom rewards. |
| `/balance` | `[user]` | View user's current GP balance. |
| `/pay` | `<user> <amount>` | Transfer server GP to another member. |
| `/daily` | *None* | Claim daily server GP reward. |
| `/flip` | `<amount> <choice>` | Wager GP on coin flip. |

---

### 🛡️️ Admin & Server Configuration (`cogs/admin/eco/` & `cogs/unity/`)

| Command | Arguments | Description |
| --- | --- | --- |
| `/config add_gp` | `<user> <amount>` | Manually award server GP to a user. |
| `/config remove_gp` | `<user> <amount>` | Deduct server GP from a user. |
| `/config reset_economy` | *None* | Reset all server GP balances. |
| `/config set_invite_reward` | `<amount>` | Set GP awarded per successful member invite. |
| `/config add_shop_item` | `<item_name> <price>` | Add or update an item in the server reward shop. |
| `/config remove_shop_item` | `<item_name>` | Remove an item from the reward shop. |
| `/config view_settings` | *None* | View server invite rewards and shop listings. |
| `/create_raffle` | `<prize> <ticket_price>` | Start a server raffle with ticket purchasing. |
| `/draw_raffle` | `<raffle_id>` | Randomly select a raffle winner. |

---

## 📝 License

Distributed under the GNU General Public License v3.0. See `LICENSE` for details.
