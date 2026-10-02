import random

# Clue Scroll Tiers and Drop Tables
CLUE_TIERS = {
    "easy": {
        "name": "Easy Clue Scroll",
        "rewards": [
            ("Bronze Trimmed Set", 15000),
            ("Black Cane", 8000),
            ("Zamorak Robe Top", 25000),
            ("Gilded Chef's Hat", 150000),
            ("Coins", 5000)
        ]
    },
    "medium": {
        "name": "Medium Clue Scroll",
        "rewards": [
            ("Ranger Boots", 35000000),
            ("Holy Sandals", 2500000),
            ("Wizard Boots", 1200000),
            ("Adamant Trimmed Set", 45000),
            ("Coins", 25000)
        ]
    },
    "hard": {
        "name": "Hard Clue Scroll",
        "rewards": [
            ("Third Age Range Top", 120000000),
            ("Robin Hood Hat", 2100000),
            ("Rune Trimmed Set", 120000),
            ("Zamorak Blessed D'hide", 350000),
            ("Coins", 75000)
        ]
    },
    "master": {
        "name": "Master Clue Scroll",
        "rewards": [
            ("Third Age Pickaxe", 2147483647),
            ("Bloodhound Pet", 500000000),
            ("Ale of the Gods", 15000000),
            ("Ankou Mask", 8000000),
            ("Coins", 250000)
        ]
    }
}

# Barrows Equipment Pool
BARROWS_EQUIPMENT = [
    ("Dharok's Helm", 1200000), ("Dharok's Platebody", 2800000), ("Dharok's Greataxe", 1500000),
    ("Karil's Leathertop", 3200000), ("Karil's Crossbow", 900000), ("Ahrim's Robetop", 4100000),
    ("Guthan's Warspear", 1800000), ("Torag's Platelegs", 600000), ("Verac's Tasset", 1100000)
]

# Boss Pets Pool: (Boss Name, Pet Name, Drop Chance 1-in-X, Bonus Reward GP)
PET_BOSSES = {
    "vorkath": ("Vorkath", "Vorki", 3000, 50000000),
    "zulrah": ("Zulrah", "Pet Snakeling", 4000, 40000000),
    "jad": ("TzTok-Jad", "TzRek-Jad", 100, 25000000),
    "corp": ("Corporeal Beast", "Pet Dark Core", 5000, 100000000),
    "cox": ("Chambers of Xeric", "Olmlet", 53, 150000000)
}