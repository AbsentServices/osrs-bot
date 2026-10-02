# Slayer Task Pool: Task Name, Min Kills, Max Kills, Reward GP per kill
SLAYER_MASTERS = {
    "turael": {
        "name": "Turael (Beginner)",
        "min_level": 1,
        "tasks": [
            ("Goblins", 15, 30, 200),
            ("Monkeys", 20, 35, 250),
            ("Skeletons", 15, 25, 300)
        ]
    },
    "vannaaka": {
        "name": "Vannaka (Intermediate)",
        "min_level": 1,
        "tasks": [
            ("Hill Giants", 30, 60, 800),
            ("Hellhounds", 40, 70, 1200),
            ("Ankou", 35, 65, 1000)
        ]
    },
    "duradel": {
        "name": "Duradel (Master)",
        "min_level": 1,
        "tasks": [
            ("Abyssal Demons", 50, 100, 3500),
            ("Dark Beasts", 40, 80, 4500),
            ("Rune Dragons", 20, 40, 8000)
        ]
    }
}

# Shared in-memory storage for active tasks: {user_id: {"task": str, "remaining": int, "reward_per_kill": int}}
active_tasks = {}