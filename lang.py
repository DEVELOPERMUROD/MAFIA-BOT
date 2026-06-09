"""
Ko'p tillilik moduli — uz / ru / en
"""

TEXTS = {
    "uz": {
        "start_private": (
            "👋 Salom, {name}!\n\n"
            "Men — Mafia o'yin botiman 🎭\n"
            "Guruhingizga qo'shing va /game bilan o'yin boshlang!\n\n"
            "📌 Buyruqlar:\n"
            "/game — yangi o'yin\n"
            "/roles — rollar haqida\n"
            "/profile — profilingiz\n"
            "/lang — til o'zgartirish"
        ),
        "start_group": "👋 Salom! /game bilan o'yin boshlang.",
        "game_already": "⚠️ Guruhda allaqachon o'yin bor. /cancel bilan bekor qiling.",
        "game_created": (
            "🎭 <b>Mafia o'yini</b>\n\n"
            "Qo'shilish uchun quyidagi tugmani bosing!\n"
            "Minimal: 4 o'yinchi\n\n"
            "👥 O'yinchilar: <b>0</b>"
        ),
        "join_btn": "🙋 Qo'shilish",
        "joined": "✅ {name} qo'shildi! ({count} o'yinchi)",
        "already_joined": "⚠️ Siz allaqachon ro'yxatdasiz.",
        "no_game": "❌ Hozir aktiv o'yin yo'q. /game bilan boshlang.",
        "not_enough": "❌ Kamida 4 o'yinchi kerak! Hozir: {count}",
        "game_started": "🎮 O'yin boshlandi! Rollar yuborilmoqda...",
        "check_pm": "📩 Rolni shaxsiy xabarda tekshiring: @{botname}",
        "pm_role": (
            "🎭 <b>Sizning rolingiz:</b>\n\n"
            "{role_emoji} <b>{role_name}</b>\n\n"
            "{role_desc}"
        ),
        "pm_mafia_list": "\n\n🤝 <b>Hammafiyadoshlaringiz:</b>\n{names}",
        "night_start": "🌙 <b>{day}-kecha boshlandi</b>\nShahar uxlaydi... 😴",
        "mafia_turn": "🔫 Mafiya: kimni o'ldirasiz?",
        "detective_turn": "🔍 Detektiv: kimni tekshirasiz?",
        "doctor_turn": "💊 Shifokor: kimni himoya qilasiz?",
        "action_confirmed": "✅ Tanlov qabul qilindi!",
        "detective_result_mafia": "🔍 <b>{name}</b> — ⚠️ MAFIYA!",
        "detective_result_clean": "🔍 <b>{name}</b> — ✅ Begunoh",
        "day_start": "☀️ <b>{day}-kun</b>\n\n{events}\n\n👥 Tirik o'yinchilar ({count}):\n{names}",
        "killed": "💀 <b>{name}</b> kechasi o'ldirildi.",
        "saved": "💊 Shifokor qutqardi! Hech kim o'lmadi.",
        "no_kill": "😮 Kechasi hech kim o'lmadi.",
        "vote_start": (
            "🗳️ <b>Ovoz berish vaqti!</b>\n"
            "Kim shahardan chiqarilsin?\n\n"
            "Har kishi bir marta ovoz beradi."
        ),
        "voted": "🗳️ {voter} → {target} ({count}/{total})",
        "vote_result": "⚖️ <b>{name}</b> ({count} ovoz) haydaldi! Roli: {role}",
        "vote_tie": "🤝 Ovozlar teng. Hech kim chiqarilmadi.",
        "vote_skip": "⏭️ Hech kim ovoz bermadi. Kecha davom etadi.",
        "town_win": "🏆 <b>Shahar g'alaba qildi!</b>\nBarcha mafiya topildi!",
        "mafia_win": "🔫 <b>Mafiya g'alaba qildi!</b>\nShahar boy berdi!",
        "all_roles": "\n\n👥 <b>Barcha rollar:</b>\n{list}",
        "play_again_btn": "🔄 Qayta o'ynash",
        "cancel_btn": "❌ Bekor qilish",
        "confirm_btn": "✅ Tasdiqlash",
        "skip_vote_btn": "⏭️ O'tkazib yuborish",
        "endvote_btn": "⚖️ Ovozni yakunlash",
        "game_cancelled": "❌ O'yin bekor qilindi.",
        "roles_text": (
            "📜 <b>Rollar</b>\n\n"
            "🔫 <b>Mafiya</b>\nHar kecha bitta shaharlini o'ldiradi. Maqsad: shaharliklardan ko'p bo'lish.\n\n"
            "🔍 <b>Detektiv</b>\nHar kecha bitta o'yinchini tekshiradi — mafiyami yoki yo'q.\n\n"
            "💊 <b>Shifokor</b>\nHar kecha bitta o'yinchini himoya qiladi.\n\n"
            "🏘️ <b>Shaharlik</b>\nMafiyadoshlarni topish uchun ovoz beradi.\n\n"
            "🏆 <b>G'alaba sharti</b>\n"
            "Shahar — barcha mafiya haydalganda\n"
            "Mafiya — mafiya soni ≥ shaharliklar soni"
        ),
        "profile_text": (
            "👤 <b>Profil</b>\n\n"
            "Ism: {name}\n"
            "O'yinlar: {games}\n"
            "G'alabalar: {wins}\n"
            "Mag'lubiyat: {losses}\n"
            "O'ldirilgan: {killed}\n\n"
            "Til: {lang}"
        ),
        "lang_changed": "✅ Til o'zgartirildi: O'zbek",
        "lang_choose": "🌐 Tilni tanlang:",
        "waiting_players": "👥 O'yinchilar ({count}):\n{names}\n\nBoshlash uchun {need} kishidan ko'p kerak.",
        "start_game_btn": "🚀 O'yinni boshlash",
        "leave_btn": "🚪 Chiqish",
        "left_game": "👋 {name} o'yindan chiqdi.",
        "cannot_leave_started": "❌ O'yin boshlangandan keyin chiqib bo'lmaydi.",
        "need_admin_to_start": "❌ Faqat /newgame buyrug'ini bergan kishi o'yinni boshlashi mumkin.",
        "bot_needs_admin": "⚠️ Iltimos, botga admin huquq bering.",
        "vote_already": "⚠️ Siz allaqachon ovoz bergansiz.",
        "not_in_game": "❌ Siz bu o'yinda emassiz.",
        "dead_cant_vote": "❌ Vafot etganlar ovoz bera olmaydi.",
        "timer_warning": "⏰ {sec} soniya qoldi!",
    },

    "ru": {
        "start_private": (
            "👋 Привет, {name}!\n\n"
            "Я — бот для игры в Мафию 🎭\n"
            "Добавь меня в группу и начни игру командой /game!\n\n"
            "📌 Команды:\n"
            "/game — новая игра\n"
            "/roles — о ролях\n"
            "/profile — ваш профиль\n"
            "/lang — сменить язык"
        ),
        "start_group": "👋 Привет! Начните игру командой /game.",
        "game_already": "⚠️ В группе уже есть игра. Отмените её командой /cancel.",
        "game_created": (
            "🎭 <b>Игра Мафия</b>\n\n"
            "Нажмите кнопку, чтобы присоединиться!\n"
            "Минимум: 4 игрока\n\n"
            "👥 Игроки: <b>0</b>"
        ),
        "join_btn": "🙋 Присоединиться",
        "joined": "✅ {name} вступил! ({count} игроков)",
        "already_joined": "⚠️ Вы уже в списке.",
        "no_game": "❌ Нет активной игры. Начните с /game.",
        "not_enough": "❌ Нужно минимум 4 игрока! Сейчас: {count}",
        "game_started": "🎮 Игра началась! Отправляю роли...",
        "check_pm": "📩 Проверьте роль в личных сообщениях: @{botname}",
        "pm_role": (
            "🎭 <b>Ваша роль:</b>\n\n"
            "{role_emoji} <b>{role_name}</b>\n\n"
            "{role_desc}"
        ),
        "pm_mafia_list": "\n\n🤝 <b>Ваши сообщники:</b>\n{names}",
        "night_start": "🌙 <b>Ночь {day}</b>\nГород спит... 😴",
        "mafia_turn": "🔫 Мафия: кого убиваете?",
        "detective_turn": "🔍 Детектив: кого проверяете?",
        "doctor_turn": "💊 Доктор: кого защищаете?",
        "action_confirmed": "✅ Выбор принят!",
        "detective_result_mafia": "🔍 <b>{name}</b> — ⚠️ МАФИЯ!",
        "detective_result_clean": "🔍 <b>{name}</b> — ✅ Мирный",
        "day_start": "☀️ <b>День {day}</b>\n\n{events}\n\n👥 Живые игроки ({count}):\n{names}",
        "killed": "💀 <b>{name}</b> был убит ночью.",
        "saved": "💊 Доктор спас жизнь! Никто не погиб.",
        "no_kill": "😮 Ночью никто не погиб.",
        "vote_start": (
            "🗳️ <b>Голосование!</b>\n"
            "Кого выгоняем из города?\n\n"
            "Каждый голосует один раз."
        ),
        "voted": "🗳️ {voter} → {target} ({count}/{total})",
        "vote_result": "⚖️ <b>{name}</b> ({count} голосов) изгнан! Роль: {role}",
        "vote_tie": "🤝 Голоса разделились. Никто не изгнан.",
        "vote_skip": "⏭️ Никто не проголосовал. Наступает ночь.",
        "town_win": "🏆 <b>Город победил!</b>\nВся мафия найдена!",
        "mafia_win": "🔫 <b>Мафия победила!</b>\nГород проиграл!",
        "all_roles": "\n\n👥 <b>Все роли:</b>\n{list}",
        "play_again_btn": "🔄 Сыграть снова",
        "cancel_btn": "❌ Отмена",
        "confirm_btn": "✅ Подтвердить",
        "skip_vote_btn": "⏭️ Пропустить",
        "endvote_btn": "⚖️ Завершить голосование",
        "game_cancelled": "❌ Игра отменена.",
        "roles_text": (
            "📜 <b>Роли</b>\n\n"
            "🔫 <b>Мафия</b>\nКаждую ночь убивает одного мирного. Цель: стать большинством.\n\n"
            "🔍 <b>Детектив</b>\nКаждую ночь проверяет одного игрока — мафия или нет.\n\n"
            "💊 <b>Доктор</b>\nКаждую ночь защищает одного игрока.\n\n"
            "🏘️ <b>Мирный</b>\nГолосует, чтобы найти мафию.\n\n"
            "🏆 <b>Победа</b>\n"
            "Город — когда вся мафия изгнана\n"
            "Мафия — когда мафия ≥ мирных"
        ),
        "profile_text": (
            "👤 <b>Профиль</b>\n\n"
            "Имя: {name}\n"
            "Игр: {games}\n"
            "Побед: {wins}\n"
            "Поражений: {losses}\n"
            "Убит раз: {killed}\n\n"
            "Язык: {lang}"
        ),
        "lang_changed": "✅ Язык изменён: Русский",
        "lang_choose": "🌐 Выберите язык:",
        "waiting_players": "👥 Игроки ({count}):\n{names}\n\nДля старта нужно ещё {need}.",
        "start_game_btn": "🚀 Начать игру",
        "leave_btn": "🚪 Выйти",
        "left_game": "👋 {name} вышел из игры.",
        "cannot_leave_started": "❌ Нельзя выйти после начала игры.",
        "need_admin_to_start": "❌ Только создатель игры может её начать.",
        "bot_needs_admin": "⚠️ Пожалуйста, дайте боту права администратора.",
        "vote_already": "⚠️ Вы уже проголосовали.",
        "not_in_game": "❌ Вы не участвуете в этой игре.",
        "dead_cant_vote": "❌ Погибшие не могут голосовать.",
        "timer_warning": "⏰ Осталось {sec} секунд!",
    },

    "en": {
        "start_private": (
            "👋 Hello, {name}!\n\n"
            "I'm a Mafia game bot 🎭\n"
            "Add me to a group and start a game with /game!\n\n"
            "📌 Commands:\n"
            "/game — new game\n"
            "/roles — about roles\n"
            "/profile — your profile\n"
            "/lang — change language"
        ),
        "start_group": "👋 Hello! Start a game with /game.",
        "game_already": "⚠️ A game already exists. Cancel it with /cancel.",
        "game_created": (
            "🎭 <b>Mafia Game</b>\n\n"
            "Press the button to join!\n"
            "Minimum: 4 players\n\n"
            "👥 Players: <b>0</b>"
        ),
        "join_btn": "🙋 Join",
        "joined": "✅ {name} joined! ({count} players)",
        "already_joined": "⚠️ You're already in the list.",
        "no_game": "❌ No active game. Start with /game.",
        "not_enough": "❌ Need at least 4 players! Now: {count}",
        "game_started": "🎮 Game started! Sending roles...",
        "check_pm": "📩 Check your role in private messages: @{botname}",
        "pm_role": (
            "🎭 <b>Your role:</b>\n\n"
            "{role_emoji} <b>{role_name}</b>\n\n"
            "{role_desc}"
        ),
        "pm_mafia_list": "\n\n🤝 <b>Your partners:</b>\n{names}",
        "night_start": "🌙 <b>Night {day}</b>\nThe city sleeps... 😴",
        "mafia_turn": "🔫 Mafia: who do you kill?",
        "detective_turn": "🔍 Detective: who do you investigate?",
        "doctor_turn": "💊 Doctor: who do you protect?",
        "action_confirmed": "✅ Selection confirmed!",
        "detective_result_mafia": "🔍 <b>{name}</b> — ⚠️ MAFIA!",
        "detective_result_clean": "🔍 <b>{name}</b> — ✅ Innocent",
        "day_start": "☀️ <b>Day {day}</b>\n\n{events}\n\n👥 Alive players ({count}):\n{names}",
        "killed": "💀 <b>{name}</b> was killed at night.",
        "saved": "💊 Doctor saved someone! Nobody died.",
        "no_kill": "😮 Nobody died last night.",
        "vote_start": (
            "🗳️ <b>Voting time!</b>\n"
            "Who gets eliminated from the city?\n\n"
            "Each person votes once."
        ),
        "voted": "🗳️ {voter} → {target} ({count}/{total})",
        "vote_result": "⚖️ <b>{name}</b> ({count} votes) eliminated! Role: {role}",
        "vote_tie": "🤝 Votes tied. Nobody was eliminated.",
        "vote_skip": "⏭️ Nobody voted. Night begins.",
        "town_win": "🏆 <b>Town wins!</b>\nAll mafia found!",
        "mafia_win": "🔫 <b>Mafia wins!</b>\nThe city fell!",
        "all_roles": "\n\n👥 <b>All roles:</b>\n{list}",
        "play_again_btn": "🔄 Play again",
        "cancel_btn": "❌ Cancel",
        "confirm_btn": "✅ Confirm",
        "skip_vote_btn": "⏭️ Skip",
        "endvote_btn": "⚖️ End voting",
        "game_cancelled": "❌ Game cancelled.",
        "roles_text": (
            "📜 <b>Roles</b>\n\n"
            "🔫 <b>Mafia</b>\nKills one townie each night. Goal: outnumber townspeople.\n\n"
            "🔍 <b>Detective</b>\nInvestigates one player each night — mafia or not.\n\n"
            "💊 <b>Doctor</b>\nProtects one player each night.\n\n"
            "🏘️ <b>Villager</b>\nVotes to find the mafia.\n\n"
            "🏆 <b>Win condition</b>\n"
            "Town — when all mafia are eliminated\n"
            "Mafia — when mafia ≥ townspeople"
        ),
        "profile_text": (
            "👤 <b>Profile</b>\n\n"
            "Name: {name}\n"
            "Games: {games}\n"
            "Wins: {wins}\n"
            "Losses: {losses}\n"
            "Times killed: {killed}\n\n"
            "Language: {lang}"
        ),
        "lang_changed": "✅ Language changed: English",
        "lang_choose": "🌐 Choose language:",
        "waiting_players": "👥 Players ({count}):\n{names}\n\nNeed {need} more to start.",
        "start_game_btn": "🚀 Start game",
        "leave_btn": "🚪 Leave",
        "left_game": "👋 {name} left the game.",
        "cannot_leave_started": "❌ Cannot leave after game started.",
        "need_admin_to_start": "❌ Only the game creator can start it.",
        "bot_needs_admin": "⚠️ Please give the bot admin permissions.",
        "vote_already": "⚠️ You already voted.",
        "not_in_game": "❌ You are not in this game.",
        "dead_cant_vote": "❌ Dead players cannot vote.",
        "timer_warning": "⏰ {sec} seconds left!",
    },
}

ROLE_INFO = {
    "uz": {
        "mafia":     ("🔫", "Mafiya",    "Har kecha bitta shaharlini o'ldiring.\nKun muhokamalarida oddiy ko'rining!"),
        "detective": ("🔍", "Detektiv",  "Har kecha bitta o'yinchini tekshiring.\nNatija faqat sizga ko'rinadi."),
        "doctor":    ("💊", "Shifokor",  "Har kecha bitta o'yinchini himoya qiling.\nO'zingizni ham himoya qila olasiz!"),
        "villager":  ("🏘️", "Shaharlik", "Mafiya kimligini aniqlang va muhokamada g'alaba qozing!"),
    },
    "ru": {
        "mafia":     ("🔫", "Мафия",    "Каждую ночь убивайте одного мирного.\nДнём притворяйтесь мирным!"),
        "detective": ("🔍", "Детектив", "Каждую ночь проверяйте игрока.\nРезультат знаете только вы."),
        "doctor":    ("💊", "Доктор",   "Каждую ночь защищайте игрока.\nМожно защищать и себя!"),
        "villager":  ("🏘️", "Мирный",  "Найдите мафию путём обсуждения!"),
    },
    "en": {
        "mafia":     ("🔫", "Mafia",     "Kill one townie each night.\nBlend in during day discussions!"),
        "detective": ("🔍", "Detective", "Investigate one player each night.\nOnly you see the result."),
        "doctor":    ("💊", "Doctor",    "Protect one player each night.\nYou can protect yourself too!"),
        "villager":  ("🏘️", "Villager", "Find the mafia through discussion!"),
    },
}

def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["uz"]).get(key, f"[{key}]")
    return text.format(**kwargs) if kwargs else text

def role_info(lang: str, role: str):
    return ROLE_INFO.get(lang, ROLE_INFO["uz"]).get(role, ("❓", role, ""))
