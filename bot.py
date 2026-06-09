"""
Mafia Telegram Boti — @MafiaBakuBlack1Bot uslubida
===================================================

O'rnatish:
    pip install python-telegram-bot==20.7

Ishga tushirish:
    export BOT_TOKEN="<tokeningiz>"
    python bot.py
"""

import os
import logging
import asyncio
from collections import Counter

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from telegram.constants import ParseMode
from telegram.error import Forbidden, BadRequest

from game import (
    Game, games, find_game_by_user,
    get_profile, update_profile, get_lang, set_lang, role_counts
)
from lang import t, role_info

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Yordamchi funksiyalar ─────────────────────────────────────────────────────

async def safe_send(bot: Bot, uid: int, text: str, **kwargs) -> bool:
    try:
        await bot.send_message(uid, text, **kwargs)
        return True
    except (Forbidden, BadRequest):
        return False

def lobby_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t(lang, "join_btn"), callback_data="lobby:join"),
            InlineKeyboardButton(t(lang, "leave_btn"), callback_data="lobby:leave"),
        ],
        [InlineKeyboardButton(t(lang, "start_game_btn"), callback_data="lobby:start")],
    ])

def lobby_text(g: Game, lang: str) -> str:
    count = len(g.players)
    mc, det, doc, vil = role_counts(count)
    names = "\n".join(f"• {p.name}" for p in g.players.values()) or "—"
    role_line = f"🔫×{mc}  🔍×{det}  💊×{doc}  🏘️×{vil}" if count >= 4 else "kamida 4 kishi kerak"
    return (
        f"🎭 <b>Mafia O'yini</b>\n\n"
        f"👥 O'yinchilar: <b>{count}</b>\n"
        f"{names}\n\n"
        f"Rollar: {role_line}"
    )

def player_kb(g: Game, action: str, exclude: list[int] = None) -> InlineKeyboardMarkup:
    exclude = exclude or []
    rows = [
        [InlineKeyboardButton(p.name, callback_data=f"{action}:{p.uid}")]
        for p in g.alive_players() if p.uid not in exclude
    ]
    return InlineKeyboardMarkup(rows)

# ── /start ────────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    name = update.effective_user.first_name
    if update.effective_chat.id == uid:
        await update.message.reply_text(
            t(lang, "start_private", name=name), parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            t(lang, "start_group"), parse_mode=ParseMode.HTML
        )

# ── /roles ────────────────────────────────────────────────────────────────────

async def cmd_roles(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    await update.message.reply_text(t(lang, "roles_text"), parse_mode=ParseMode.HTML)

# ── /profile ──────────────────────────────────────────────────────────────────

async def cmd_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    p = get_profile(uid)
    lang_names = {"uz": "O'zbek 🇺🇿", "ru": "Русский 🇷🇺", "en": "English 🇬🇧"}
    await update.message.reply_text(
        t(lang, "profile_text",
          name=update.effective_user.first_name,
          games=p.get("games", 0),
          wins=p.get("wins", 0),
          losses=p.get("losses", 0),
          killed=p.get("killed", 0),
          lang=lang_names.get(p.get("lang", "uz"), "O'zbek 🇺🇿")),
        parse_mode=ParseMode.HTML
    )

# ── /lang ─────────────────────────────────────────────────────────────────────

async def cmd_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang:uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang:en"),
        ]
    ])
    await update.message.reply_text(t(lang, "lang_choose"), reply_markup=kb)

# ── /game ─────────────────────────────────────────────────────────────────────

async def cmd_game(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    uid = update.effective_user.id
    lang = get_lang(uid)

    if cid == uid:
        await update.message.reply_text("❌ Bu komanda faqat guruhda ishlaydi.")
        return
    if cid in games:
        await update.message.reply_text(t(lang, "game_already"))
        return

    g = Game(cid, uid)
    games[cid] = g
    msg = await update.message.reply_text(
        lobby_text(g, lang),
        reply_markup=lobby_keyboard(lang),
        parse_mode=ParseMode.HTML
    )
    g.lobby_msg_id = msg.message_id

# ── /cancel ───────────────────────────────────────────────────────────────────

async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    uid = update.effective_user.id
    lang = get_lang(uid)
    if cid not in games:
        await update.message.reply_text(t(lang, "no_game"))
        return
    g = games[cid]
    if not g.is_creator(uid):
        await update.message.reply_text(t(lang, "need_admin_to_start"))
        return
    del games[cid]
    await update.message.reply_text(t(lang, "game_cancelled"))

# ── /vote ─────────────────────────────────────────────────────────────────────

async def cmd_vote(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    uid = update.effective_user.id
    lang = get_lang(uid)
    if cid not in games or games[cid].phase != "day":
        await update.message.reply_text("❌ Hozir ovoz berish mumkin emas.")
        return
    await start_vote(cid, ctx)

# ── /endvote ──────────────────────────────────────────────────────────────────

async def cmd_endvote(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    uid = update.effective_user.id
    lang = get_lang(uid)
    if cid not in games or games[cid].phase != "vote":
        return
    g = games[cid]
    if not g.is_creator(uid):
        await update.message.reply_text(t(lang, "need_admin_to_start"))
        return
    await tally_votes(cid, ctx)

# ── Lobby tugmalari ───────────────────────────────────────────────────────────

async def lobby_join(q, uid: int, cid: int, ctx):
    lang = get_lang(uid)
    g = games[cid]
    name = q.from_user.first_name
    if uid in g.players:
        await q.answer(t(lang, "already_joined"), show_alert=True)
        return
    if len(g.players) >= 12:
        await q.answer("❌ To'ldi (max 12)", show_alert=True)
        return
    g.players[uid] = type("P", (), {"uid": uid, "name": name, "role": None, "alive": True})()
    # Player class ishlatamiz
    from game import Player
    g.players[uid] = Player(uid, name)
    await q.answer(f"✅ Qo'shildingiz!")
    # Lobby xabarini yangilash
    try:
        await ctx.bot.edit_message_text(
            chat_id=cid,
            message_id=g.lobby_msg_id,
            text=lobby_text(g, lang),
            reply_markup=lobby_keyboard(lang),
            parse_mode=ParseMode.HTML
        )
    except BadRequest:
        pass
    await ctx.bot.send_message(
        cid, t(lang, "joined", name=name, count=len(g.players)),
        parse_mode=ParseMode.HTML
    )

async def lobby_leave(q, uid: int, cid: int, ctx):
    lang = get_lang(uid)
    g = games[cid]
    if uid not in g.players:
        await q.answer("Siz ro'yxatda emassiz.", show_alert=True)
        return
    if g.phase != "lobby":
        await q.answer(t(lang, "cannot_leave_started"), show_alert=True)
        return
    name = g.players[uid].name
    del g.players[uid]
    await q.answer("Chiqtingiz")
    try:
        await ctx.bot.edit_message_text(
            chat_id=cid, message_id=g.lobby_msg_id,
            text=lobby_text(g, lang), reply_markup=lobby_keyboard(lang),
            parse_mode=ParseMode.HTML
        )
    except BadRequest:
        pass
    await ctx.bot.send_message(cid, t(lang, "left_game", name=name))

async def lobby_start(q, uid: int, cid: int, ctx):
    lang = get_lang(uid)
    g = games[cid]
    if not g.is_creator(uid):
        await q.answer(t(lang, "need_admin_to_start"), show_alert=True)
        return
    if len(g.players) < 4:
        await q.answer(t(lang, "not_enough", count=len(g.players)), show_alert=True)
        return

    g.assign_roles()
    g.phase = "started"
    await q.answer("🚀 Boshlandi!")

    # Lobby xabarini o'chirish / yangilash
    try:
        await ctx.bot.edit_message_text(
            chat_id=cid, message_id=g.lobby_msg_id,
            text=t(lang, "game_started"), parse_mode=ParseMode.HTML
        )
    except BadRequest:
        pass

    botname = (await ctx.bot.get_me()).username
    # Rolllarni shaxsiy xabarda yuborish
    failed = []
    mafia_ids = [p.uid for p in g.role_players("mafia")]
    mafia_names = ", ".join(g.players[m].name for m in mafia_ids)

    for p in g.players.values():
        emoji, rname, rdesc = role_info(lang, p.role)
        text = t(lang, "pm_role", role_emoji=emoji, role_name=rname, role_desc=rdesc)
        if p.role == "mafia" and len(mafia_ids) > 1:
            partners = [g.players[m].name for m in mafia_ids if m != p.uid]
            text += t(lang, "pm_mafia_list", names="\n".join(f"• {n}" for n in partners))
        sent = await safe_send(ctx.bot, p.uid, text, parse_mode=ParseMode.HTML)
        if not sent:
            failed.append(p.name)

    if failed:
        await ctx.bot.send_message(
            cid,
            f"⚠️ Quyidagilarga shaxsiy xabar yuborib bo'lmadi:\n"
            f"{', '.join(failed)}\n\n"
            f"Iltimos, @{botname} bilan shaxsiy chat oching va /start bosing.",
        )

    for p in g.players.values():
        update_profile(p.uid, games=1)

    await ctx.bot.send_message(
        cid, t(lang, "check_pm", botname=botname), parse_mode=ParseMode.HTML
    )
    await asyncio.sleep(3)
    await start_night(cid, ctx)

# ── Kecha ─────────────────────────────────────────────────────────────────────

async def start_night(cid: int, ctx: ContextTypes.DEFAULT_TYPE):
    g = games[cid]
    g.phase = "night"
    g.day += 1
    g.reset_night()
    lang = get_lang(g.creator_id)

    await ctx.bot.send_message(
        cid, t(lang, "night_start", day=g.day), parse_mode=ParseMode.HTML
    )

    alive = g.alive_ids()
    # Mafiya
    mafia = g.role_players("mafia")
    if mafia:
        g.pending_night.add("mafia")
        non_mafia = [p for p in g.alive_players() if p.role != "mafia"]
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(p.name, callback_data=f"nkill:{p.uid}")]
            for p in non_mafia
        ])
        for m in mafia:
            await safe_send(ctx.bot, m.uid,
                f"🌙 <b>{g.day}-kecha</b>\n" + t(lang, "mafia_turn"),
                parse_mode=ParseMode.HTML, reply_markup=kb)

    # Detektiv
    dets = g.role_players("detective")
    if dets:
        g.pending_night.add("detective")
        det = dets[0]
        others = [p for p in g.alive_players() if p.uid != det.uid]
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(p.name, callback_data=f"ncheck:{p.uid}")]
            for p in others
        ])
        await safe_send(ctx.bot, det.uid,
            f"🌙 <b>{g.day}-kecha</b>\n" + t(lang, "detective_turn"),
            parse_mode=ParseMode.HTML, reply_markup=kb)

    # Shifokor
    docs = g.role_players("doctor")
    if docs:
        g.pending_night.add("doctor")
        doc = docs[0]
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(p.name, callback_data=f"nsave:{p.uid}")]
            for p in g.alive_players()
        ])
        await safe_send(ctx.bot, doc.uid,
            f"🌙 <b>{g.day}-kecha</b>\n" + t(lang, "doctor_turn"),
            parse_mode=ParseMode.HTML, reply_markup=kb)

async def maybe_end_night(g: Game, ctx: ContextTypes.DEFAULT_TYPE):
    if g.pending_night:
        return

    cid = g.chat_id
    lang = get_lang(g.creator_id)

    # Detektiv natijasi
    if g.night_check is not None:
        dets = g.role_players("detective")
        if dets:
            target = g.players.get(g.night_check)
            if target:
                is_mafia = target.role == "mafia"
                key = "detective_result_mafia" if is_mafia else "detective_result_clean"
                await safe_send(ctx.bot, dets[0].uid,
                    t(lang, key, name=target.name), parse_mode=ParseMode.HTML)

    killed_uid, saved_uid = g.resolve_night()
    events = []

    if killed_uid is not None:
        p = g.players[killed_uid]
        events.append(t(lang, "killed", name=p.name))
        update_profile(killed_uid, killed=1)
    elif saved_uid is not None and g.night_kills:
        events.append(t(lang, "saved"))
    else:
        events.append(t(lang, "no_kill"))

    winner = g.check_win()
    if winner:
        await end_game(cid, ctx, winner, extra_event="\n".join(events))
        return

    g.phase = "day"
    alive = g.alive_players()
    names = "\n".join(f"• {p.name}" for p in alive)
    await ctx.bot.send_message(
        cid,
        t(lang, "day_start",
          day=g.day,
          events="\n".join(events),
          count=len(alive),
          names=names),
        parse_mode=ParseMode.HTML
    )

# ── Kun / ovoz berish ─────────────────────────────────────────────────────────

async def start_vote(cid: int, ctx: ContextTypes.DEFAULT_TYPE):
    g = games[cid]
    lang = get_lang(g.creator_id)
    g.phase = "vote"
    g.votes = {}
    kb_rows = [
        [InlineKeyboardButton(p.name, callback_data=f"vote:{p.uid}")]
        for p in g.alive_players()
    ]
    kb_rows.append([
        InlineKeyboardButton(t(lang, "skip_vote_btn"), callback_data="vote:skip"),
        InlineKeyboardButton(t(lang, "endvote_btn"),   callback_data="vote:end"),
    ])
    msg = await ctx.bot.send_message(
        cid, t(lang, "vote_start"),
        reply_markup=InlineKeyboardMarkup(kb_rows),
        parse_mode=ParseMode.HTML
    )
    g.vote_msg_id = msg.message_id

async def tally_votes(cid: int, ctx: ContextTypes.DEFAULT_TYPE):
    g = games[cid]
    lang = get_lang(g.creator_id)

    if not g.votes:
        await ctx.bot.send_message(cid, t(lang, "vote_skip"))
        await start_night(cid, ctx)
        return

    c = Counter(g.votes.values())
    top_id, top_count = c.most_common(1)[0]

    # Teng bo'lsa
    if len(c) > 1:
        counts = list(c.values())
        if counts[0] == counts[1]:
            await ctx.bot.send_message(cid, t(lang, "vote_tie"))
            await start_night(cid, ctx)
            return

    target = g.players[top_id]
    target.alive = False
    emoji, rname, _ = role_info(lang, target.role)
    await ctx.bot.send_message(
        cid,
        t(lang, "vote_result",
          name=target.name, count=top_count, role=f"{emoji} {rname}"),
        parse_mode=ParseMode.HTML
    )

    winner = g.check_win()
    if winner:
        await end_game(cid, ctx, winner)
        return

    await start_night(cid, ctx)

# ── O'yin tugashi ─────────────────────────────────────────────────────────────

async def end_game(cid: int, ctx: ContextTypes.DEFAULT_TYPE, winner: str, extra_event: str = ""):
    g = games.get(cid)
    if not g:
        return
    lang = get_lang(g.creator_id)
    g.phase = "ended"

    win_key = "town_win" if winner == "town" else "mafia_win"
    text = t(lang, win_key)

    # Barcha rollar
    role_list = "\n".join(
        f"{'✅' if p.alive else '💀'} {p.name} — "
        f"{role_info(lang, p.role)[0]} {role_info(lang, p.role)[1]}"
        for p in g.players.values()
    )
    text += t(lang, "all_roles", list=role_list)

    if extra_event:
        text = extra_event + "\n\n" + text

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "play_again_btn"), callback_data="newgame:start")]
    ])

    await ctx.bot.send_message(cid, text, parse_mode=ParseMode.HTML, reply_markup=kb)

    # Profil yangilash
    for p in g.players.values():
        if winner == "town":
            if p.role != "mafia":
                update_profile(p.uid, wins=1)
            else:
                update_profile(p.uid, losses=1)
        else:
            if p.role == "mafia":
                update_profile(p.uid, wins=1)
            else:
                update_profile(p.uid, losses=1)

    del games[cid]

# ── Callback handler ──────────────────────────────────────────────────────────

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    cid = q.message.chat_id
    data = q.data
    lang = get_lang(uid)

    # Til
    if data.startswith("lang:"):
        new_lang = data.split(":")[1]
        set_lang(uid, new_lang)
        await q.edit_message_text(t(new_lang, "lang_changed"))
        return

    # Qayta o'ynash
    if data == "newgame:start":
        if cid in games:
            await q.answer("O'yin allaqachon bor.", show_alert=True)
            return
        g = Game(cid, uid)
        games[cid] = g
        msg = await ctx.bot.send_message(
            cid, lobby_text(g, lang),
            reply_markup=lobby_keyboard(lang),
            parse_mode=ParseMode.HTML
        )
        g.lobby_msg_id = msg.message_id
        return

    # Lobby
    if data.startswith("lobby:"):
        action = data.split(":")[1]
        if cid not in games:
            await q.answer(t(lang, "no_game"), show_alert=True)
            return
        g = games[cid]
        if g.phase != "lobby":
            await q.answer("O'yin boshlangan.", show_alert=True)
            return
        if action == "join":
            await lobby_join(q, uid, cid, ctx)
        elif action == "leave":
            await lobby_leave(q, uid, cid, ctx)
        elif action == "start":
            await lobby_start(q, uid, cid, ctx)
        return

    # Ovoz berish
    if data.startswith("vote:"):
        val = data.split(":")[1]
        if cid not in games:
            return
        g = games[cid]
        if g.phase != "vote":
            return

        if val == "skip":
            if g.is_creator(uid):
                await tally_votes(cid, ctx)
            else:
                await q.answer("Faqat moderator o'tkaza oladi.", show_alert=True)
            return
        if val == "end":
            if g.is_creator(uid):
                await tally_votes(cid, ctx)
            else:
                await q.answer("Faqat moderator tugatishi mumkin.", show_alert=True)
            return

        target_id = int(val)
        if uid not in g.players or not g.players[uid].alive:
            await q.answer(t(lang, "not_in_game"), show_alert=True)
            return
        if uid in g.votes:
            await q.answer(t(lang, "vote_already"), show_alert=True)
            return

        g.votes[uid] = target_id
        voter_name = g.players[uid].name
        target_name = g.players[target_id].name
        total = len(g.alive_players())
        await ctx.bot.send_message(
            cid,
            t(lang, "voted", voter=voter_name, target=target_name,
              count=len(g.votes), total=total),
        )
        if len(g.votes) >= total:
            await tally_votes(cid, ctx)
        return

    # Kecha harakatlari (shaxsiy xabar orqali)
    if data.startswith("nkill:"):
        target_id = int(data.split(":")[1])
        g = find_game_by_user(uid)
        if not g or g.phase != "night":
            return
        if uid not in [p.uid for p in g.role_players("mafia")]:
            return
        g.night_kills[uid] = target_id
        # Barcha mafiya ovoz bergandami
        mafia_ids = {p.uid for p in g.role_players("mafia")}
        if mafia_ids.issubset(set(g.night_kills.keys())):
            g.pending_night.discard("mafia")
        await q.edit_message_text(t(lang, "action_confirmed"), parse_mode=ParseMode.HTML)
        await maybe_end_night(g, ctx)
        return

    if data.startswith("ncheck:"):
        target_id = int(data.split(":")[1])
        g = find_game_by_user(uid)
        if not g or g.phase != "night":
            return
        g.night_check = target_id
        g.pending_night.discard("detective")
        await q.edit_message_text(t(lang, "action_confirmed"))
        await maybe_end_night(g, ctx)
        return

    if data.startswith("nsave:"):
        target_id = int(data.split(":")[1])
        g = find_game_by_user(uid)
        if not g or g.phase != "night":
            return
        g.night_save = target_id
        g.pending_night.discard("doctor")
        await q.edit_message_text(t(lang, "action_confirmed"))
        await maybe_end_night(g, ctx)
        return

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN topilmadi!\n   export BOT_TOKEN=<tokeningiz>")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start",    cmd_start))
    app.add_handler(CommandHandler("game",     cmd_game))
    app.add_handler(CommandHandler("cancel",   cmd_cancel))
    app.add_handler(CommandHandler("roles",    cmd_roles))
    app.add_handler(CommandHandler("profile",  cmd_profile))
    app.add_handler(CommandHandler("lang",     cmd_lang))
    app.add_handler(CommandHandler("vote",     cmd_vote))
    app.add_handler(CommandHandler("endvote",  cmd_endvote))
    app.add_handler(CallbackQueryHandler(on_callback))

    print("🎭 Mafia boti ishga tushdi!")
    print("Buyruqlar: /game /roles /profile /lang /cancel /vote /endvote")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
