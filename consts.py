RANKUP_PROGRESSION = {
    "Noob": {
        "next_rank": "Pro",
        "ticket_cost": 50,
        "difficulty": "EASY",
    },
    "Pro": {
        "next_rank": "Master",
        "ticket_cost": 100,
        "difficulty": "MEDIUM",
    },
    "Master": {
        "next_rank": "Champion",
        "ticket_cost": 150,
        "difficulty": "HARD",
    },
    "Champion": {
        "next_rank": "Champion",
        "ticket_cost": 150,
        "difficulty": "HARD",
    }
}

RANKDOWN_PROGRESSION = {
    "Champion": "Master",
    "Master": "Pro",
    "Pro": "Noob",
    "Noob": "Noob"
}

RANK_VALUE = {
    "Noob": 1,
    "Pro": 2,
    "Master": 3,
    "Champion": 4
}

BATTLE_TIMEOUT = 60 * 60
RANKUP_TIMEOUT = 60 * 25
BATTLE_REQUEST_TIMEOUT = 60 * 2
BATTLE_CANCEL_REQUEST_TIMEOUT = 60