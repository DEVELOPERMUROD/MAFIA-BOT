# 🎭 Mafia Telegram Boti

@MafiaBakuBlack1Bot uslubidagi to'liq Mafia o'yini boti.

## Xususiyatlar
- 🌐 **3 til**: O'zbek, Rus, Ingliz (`/lang`)
- 👤 **Profil tizimi**: o'yinlar, g'alabalar, mag'lubiyat statistikasi (`/profile`)
- 🎭 **4 rol**: Mafiya, Detektiv, Shifokor, Shaharlik
- 🔘 **Inline tugmalar**: barcha harakatlar tugmalar orqali
- 🌙 **Shaxsiy xabarlar**: rollar va kecha harakatlari PM orqali
- 👥 **4–12 o'yinchi** qo'llab-quvvatlanadi

## O'rnatish

```bash
pip install -r requirements.txt
```

## Ishga tushirish

```bash
export BOT_TOKEN="<@BotFather dan olgan tokeningiz>"
python bot.py
```

Yoki Windows:
```
set BOT_TOKEN=<tokeningiz>
python bot.py
```

## Token olish

1. Telegramda [@BotFather](https://t.me/BotFather) ga yozing
2. `/newbot` buyrug'ini bering
3. Bot nomi va username kiriting
4. Token nusxa oling

## Guruhda botni sozlash

1. Botni guruhga qo'shing
2. Botga **Admin huquq** bering (xabar o'chirish uchun)
3. `/game` bilan o'yin boshlang

## Buyruqlar

| Buyruq | Vazifasi |
|--------|----------|
| `/game` | Yangi o'yin yaratish |
| `/cancel` | O'yinni bekor qilish |
| `/vote` | Ovoz berish boshlash |
| `/endvote` | Ovoz berishni yakunlash |
| `/roles` | Rollar haqida |
| `/profile` | Shaxsiy statistika |
| `/lang` | Tilni o'zgartirish |

## O'yin qoidalari

**Rollar:**
- 🔫 **Mafiya** — har kecha bitta shaharlini o'ldiradi
- 🔍 **Detektiv** — har kecha bitta o'yinchini tekshiradi
- 💊 **Shifokor** — har kecha bitta o'yinchini himoya qiladi
- 🏘️ **Shaharlik** — mafiyadoshlarni muhokama orqali topadi

**O'yinchilar soni bo'yicha rollar:**
| O'yinchilar | Mafiya | Detektiv | Shifokor |
|-------------|--------|----------|----------|
| 4 | 1 | — | — |
| 5 | 1 | 1 | — |
| 6–8 | 2 | 1 | 1 |
| 9–12 | 3 | 1 | 1 |

## Fayl tuzilmasi

```
mafia_bot/
├── bot.py          # Asosiy bot fayli
├── game.py         # O'yin holati va mantiq
├── lang.py         # Tarjimalar (uz/ru/en)
├── requirements.txt
├── profiles.json   # Profil ma'lumotlari (avtomatik yaratiladi)
└── README.md
```
