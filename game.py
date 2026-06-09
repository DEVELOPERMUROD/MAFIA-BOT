"""
O'yin holati va mantiq
"""

import random
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Profil saqlash (JSON fayl) ───────────────────────────────────────────────

PROFILE_FILE = "profiles.json"

def load_profiles() -> dict:
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_profiles(profiles: dict):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

def get_profile(uid: int) -> dict:
    profiles = load_profiles()
    key = str(uid)
    if key not in profiles:
        profiles[key] = {"games": 0, "wins": 0, "losses": 0, "killed": 0, "lang": "uz"}
        save_profiles(profiles)
    return profiles[key]

def update_profile(uid: int, **kwargs):
    profiles = load_profiles()
    key = str(uid)
    if key not in profiles:
        profiles[key] = {"games": 0, "wins": 0, "losses": 0, "killed": 0, "lang": "uz"}
    for k, v in kwargs.items():
        if k in ("games", "wins", "losses", "killed"):
            profiles[key][k] = profiles[key].get(k, 0) + v
        else:
            profiles[key][k] = v
    save_profiles(profiles)

def get_lang(uid: int) -> str:
    return get_profile(uid).get("lang", "uz")

def set_lang(uid: int, lang: str):
    update_profile(uid, lang=lang)

# ── O'yin holati ─────────────────────────────────────────────────────────────

PHASES = ["lobby", "night", "day", "vote", "ended"]

class Player:
    def __init__(self, uid: int, name: str):
        self.uid = uid
        self.name = name
        self.role: Optional[str] = None
        self.alive: bool = True

class Game:
    def __init__(self, chat_id: int, creator_id: int):
        self.chat_id = chat_id
        self.creator_id = creator_id
        self.phase = "lobby"
        self.players: dict[int, Player] = {}   # uid -> Player
        self.day = 0
        self.lobby_msg_id: Optional[int] = None  # lobby xabarini tahrirlash uchun

        # Kecha
        self.night_kills: dict[int, int] = {}   # mafia_uid -> target_uid
        self.night_save: Optional[int] = None
        self.night_check: Optional[int] = None
        self.pending_night: set[str] = set()

        # Kun
        self.votes: dict[int, int] = {}          # voter_uid -> target_uid
        self.vote_msg_id: Optional[int] = None

    # ── Yordamchilar ─────────────────────────────────────────────────────────

    def alive_players(self) -> list[Player]:
        return [p for p in self.players.values() if p.alive]

    def alive_ids(self) -> list[int]:
        return [p.uid for p in self.alive_players()]

    def role_players(self, role: str, alive_only=True) -> list[Player]:
        ps = self.alive_players() if alive_only else list(self.players.values())
        return [p for p in ps if p.role == role]

    def is_creator(self, uid: int) -> bool:
        return uid == self.creator_id

    def check_win(self) -> Optional[str]:
        alive = self.alive_players()
        mafia = [p for p in alive if p.role == "mafia"]
        town  = [p for p in alive if p.role != "mafia"]
        if not mafia:
            return "town"
        if len(mafia) >= len(town):
            return "mafia"
        return None

    # ── Rol taqsimlash ───────────────────────────────────────────────────────

    def assign_roles(self):
        ids = list(self.players.keys())
        n = len(ids)
        mc = 1 if n <= 5 else (2 if n <= 8 else 3)
        roles = ["mafia"] * mc
        if n >= 5: roles.append("detective")
        if n >= 6: roles.append("doctor")
        while len(roles) < n:
            roles.append("villager")
        random.shuffle(roles)
        for uid, role in zip(ids, roles):
            self.players[uid].role = role

    # ── Kecha natijasi ───────────────────────────────────────────────────────

    def resolve_night(self) -> tuple[Optional[int], Optional[int]]:
        """
        Returns: (killed_uid_or_None, saved_uid_or_None)
        """
        if not self.night_kills:
            return None, self.night_save

        from collections import Counter
        c = Counter(self.night_kills.values())
        target = c.most_common(1)[0][0]

        if target == self.night_save:
            return None, target   # saved

        self.players[target].alive = False
        return target, self.night_save

    def reset_night(self):
        self.night_kills = {}
        self.night_save = None
        self.night_check = None
        self.pending_night = set()
        self.votes = {}

# ── Global o'yin xotirasi ────────────────────────────────────────────────────

games: dict[int, Game] = {}   # chat_id -> Game

def find_game_by_user(uid: int) -> Optional[Game]:
    for g in games.values():
        if uid in g.players and g.phase == "night":
            return g
    return None

def role_counts(n: int) -> tuple[int, int, int, int]:
    """mafia, detective, doctor, villager counts"""
    mc = 1 if n <= 5 else (2 if n <= 8 else 3)
    det = 1 if n >= 5 else 0
    doc = 1 if n >= 6 else 0
    vil = n - mc - det - doc
    return mc, det, doc, vil
