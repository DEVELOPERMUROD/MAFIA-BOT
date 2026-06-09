"""
Admin panel moduli — faqat Telegram
"""

import os
from game import games, load_profiles

# ── Admin ID ──────────────────────────────────────────────────────────────────
ADMIN_IDS_RAW = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS: set[int] = set()
for x in ADMIN_IDS_RAW.split(","):
    x = x.strip()
    if x.isdigit():
        ADMIN_IDS.add(int(x))

BOT_ENABLED = {"value": True}


def is_admin(uid: int) -> bool:
    return uid in ADMIN_IDS
