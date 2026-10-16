import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
SITE_URL = os.getenv("PUBLIC_BASE_URL", "https://example.com").strip().rstrip("/")
ADMIN_IDS = {
    int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
}
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("cpm1-premium")

DISCLAIMER = (
    "\n\n⚠️ Бұл бот CPM ойынының ішкі деректерін тікелей өзгертпейді. "
    "Ойын ішіндегі функциялар тек ресми API немесе рұқсат етілген интеграция арқылы іске аса алады. "
    "Құпиясөздер мен растау кодтарын ешкімге берме."
)

MENU = {
    "economy": ("💰 ECONOMY MENU", [
        ("💸 Set Money", "demo_money"),
        ("💰 Set Coins", "demo_coins"),
    ]),
    "premium": ("⭐ PREMIUM FEATURES", [
        ("👑 King Rank", "demo_king"),
        ("🚗 Unlock All Cars", "demo_cars"),
        ("🏠 Unlock Houses", "demo_houses"),
        ("🛞 Unlock Wheels", "demo_wheels"),
        ("💨 Smoke & Effects", "demo_effects"),
        ("📯 Horns & Lights", "demo_lights"),
        ("🏆 Levels", "demo_levels"),
        ("⚡ Unlock Everything", "demo_everything"),
    ]),
    "chrome": ("🪞 CHROME MENU", [
        ("🚘 Chrome Car", "demo_chrome_car"),
        ("🪟 Chrome Windows", "demo_chrome_windows"),
        ("💡 Chrome Headlights", "demo_chrome_lights"),
        ("🛞 Chrome Wheels", "demo_chrome_wheels"),
        ("🌟 Full Chrome", "demo_full_chrome"),
        ("♻️ Reset Chrome", "demo_reset_chrome"),
    ]),
    "cars": ("🚗 CAR UNLOCK MENU", [
        ("🆔 Unlock Car by ID", "demo_car_id"),
        ("🚀 All Cars", "demo_all_cars"),
    ]),
    "vinyl": ("🎨 COPY VINYL TOOLS", [
        ("🎭 Copy Vinyl Between Cars", "demo_vinyl"),
        ("📤 Copy Vinyl to Multiple Cars", "demo_vinyl_multi"),
        ("🌍 Copy Vinyl to All Cars", "demo_vinyl_all"),
    ]),
    "copy": ("🚘 CAR COPY", [
        ("🚗 Copy One Car", "demo_copy_car"),
        ("📦 Copy All Cars", "demo_copy_all"),
        ("💙 Account Cloner", "demo_clone"),
    ]),
    "account": ("⚙️ ACCOUNT SETTINGS", [
        ("✏️ Change Name", "demo_name"),
        ("🆔 Change CPM ID", "demo_id"),
        ("📧 Change Email", "demo_email"),
        ("🔐 Change Password", "demo_password"),
        ("🏁 Race Stats", "demo_stats"),
        ("🚘 Number Plates", "demo_plates"),
    ]),
    "siren": ("🚨 SIREN MENU", [
        ("🚔 Siren for One Car", "demo_siren_car"),
        ("😀 Sirens for All Cars", "demo_siren_all"),
    ]),
    "bumper": ("🔧 REMOVE BUMPER MENU", [
        ("✔️ Front Bumper", "demo_bumper_front"),
        ("✔️ Rear Bumper", "demo_bumper_rear"),
        ("✔️ Both Bumpers", "demo_bumper_both"),
        ("✔️ All Cars", "demo_bumper_all"),
    ]),
}

MAIN_KEYS = [
    [("💰 ECONOMY MENU", "menu:economy"), ("⭐ PREMIUM FEATURES", "menu:premium")],
    [("🪞 CHROME MENU", "menu:chrome"), ("🚗 CAR UNLOCK", "menu:cars")],
    [("🎨 VINYL TOOLS", "menu:vinyl"), ("🚘 CAR COPY", "menu:copy")],
    [("⚙️ ACCOUNT SETTINGS", "menu:account")],
    [("🚨 SIREN MENU", "menu:siren"), ("🔧 REMOVE BUMPER", "menu:bumper")],
    [("🛒 CPM MARKETPLACE", "market"), ("🛡️ SAFETY / HELP", "help")],
]

SAFE_TEXT = {
    "demo_money": "💸 *Set Money*\nБұл бөлімнің интерфейсі дайын. Ойын валютасын өзгертуге ресми, рұқсат етілген API қажет.",
    "demo_coins": "💰 *Set Coins*\nБұл батырма әзірге демо режимінде. Ойынның қорғанысын айналып өту әрекеті жасалмайды.",
    "demo_king": "👑 *King Rank*\nРангты өзгерту функциясы ресми интеграция болғанда ғана қосылады.",
    "demo_cars": "🚗 *Unlock All Cars*\nКөлік құлпын ойын ішінде автоматты ашу бұл шаблонда орындалмайды.",
    "demo_houses": "🏠 *Unlock Houses*\nОйын қолдайтын ресми әдіс болмаса, үйлерді автоматты ашу мүмкін емес.",
    "demo_wheels": "🛞 *Unlock Wheels*\nБұл — интерфейс демосы. Ойын деректеріне өзгеріс енгізілмейді.",
    "demo_effects": "💨 *Smoke & Effects*\nЭффектілер мәзірі дайын; нақты басқару үшін ресми интеграция қажет.",
    "demo_lights": "📯 *Horns & Lights*\nБұл батырма әзірге ақпараттық бөлім ретінде жұмыс істейді.",
    "demo_levels": "🏆 *Levels*\nДеңгейлерді өзгерту немесе аяқтау бұл нұсқада орындалмайды.",
    "demo_everything": "⚡ *Unlock Everything*\nБір батырмамен ойын ішін өзгерту іске қосылмаған. Тек рұқсат етілген ресми интеграцияны қолдану керек.",
    "demo_chrome_car": "🚘 *Chrome Car*\nChrome баптауы интерфейсте көрсетіледі; ойынға өзгеріс жіберілмейді.",
    "demo_chrome_windows": "🪟 *Chrome Windows*\nБұл функция әзірге демо.",
    "demo_chrome_lights": "💡 *Chrome Headlights*\nБұл функция әзірге демо.",
    "demo_chrome_wheels": "🛞 *Chrome Wheels*\nБұл функция әзірге демо.",
    "demo_full_chrome": "🌟 *Full Chrome*\nБарлық бөлшекті автоматты өзгерту іске қосылмаған.",
    "demo_reset_chrome": "♻️ *Reset Chrome*\nҚалпына келтіру үшін ойын ішіндегі ресми баптауларды пайдалан.",
    "demo_car_id": "🆔 *Unlock Car by ID*\nМашина ID-сін өңдеу бұл ботта орындалмайды; ресми API қажет.",
    "demo_all_cars": "🚀 *All Cars*\nБұл батырма интерфейс демосы ғана.",
    "demo_vinyl": "🎭 *Copy Vinyl*\nВинилді көшіру ойындағы ресми мүмкіндіктермен ғана орындалуы тиіс.",
    "demo_vinyl_multi": "📤 *Copy Vinyl to Multiple Cars*\nБұл функция интерфейс демосы.",
    "demo_vinyl_all": "🌍 *Copy Vinyl to All Cars*\nБұл функция интерфейс демосы.",
    "demo_copy_car": "🚗 *Copy One Car*\nБасқа аккаунтқа машина көшіру үшін ресми, рұқсат етілген интеграция қажет.",
    "demo_copy_all": "📦 *Copy All Cars*\nБұл бот ойын аккаунттарының деректерін көшірмейді.",
    "demo_clone": "💙 *Account Cloner*\nАккаунтты клондау немесе рұқсатсыз көшіру қолжетімді емес. Ешқашан логин/құпиясөз жіберме.",
    "demo_name": "✏️ *Change Name*\nОйын ішіндегі ресми профиль баптауларын қолдан.",
    "demo_id": "🆔 *Change CPM ID*\nCPM ID өзгерту бұл ботта орындалмайды.",
    "demo_email": "📧 *Change Email*\nEmail ауыстыруды тек ойынның ресми аккаунт баптауларында орында.",
    "demo_password": "🔐 *Change Password*\nҚұпиясөзді тек ресми қолданбада ауыстыр. Ботқа құпиясөзді жазба.",
    "demo_stats": "🏁 *Race Stats*\nЖеңіс/жеңіліс статистикасын өңдеу бұл шаблонда орындалмайды.",
    "demo_plates": "🚘 *Number Plates*\nНөмірді ойын ішіндегі рұқсат етілген баптаулардан өзгертіңіз.",
    "demo_siren_car": "🚔 *Siren for One Car*\nСирена орнату үшін ойынның ресми мүмкіндіктерін пайдаланыңыз.",
    "demo_siren_all": "😀 *Sirens for All Cars*\nБұл функция интерфейс демосы.",
    "demo_bumper_front": "✔️ *Front Bumper*\nБамперді өзгерту бұл ботта орындалмайды.",
    "demo_bumper_rear": "✔️ *Rear Bumper*\nБамперді өзгерту бұл ботта орындалмайды.",
    "demo_bumper_both": "✔️ *Both Bumpers*\nБамперді өзгерту бұл ботта орындалмайды.",
    "demo_bumper_all": "✔️ *All Cars*\nБұл функция интерфейс демосы.",
}

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=cb) for text, cb in row]
        for row in MAIN_KEYS
    ])

def section_keyboard(key):
    title, items = MENU[key]
    rows = []
    for i in range(0, len(items), 2):
        rows.append([InlineKeyboardButton(t, callback_data=c) for t, c in items[i:i+2]])
    rows.append([InlineKeyboardButton("⬅️ BACK TO MAIN MENU", callback_data="home")])
    return InlineKeyboardMarkup(rows)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 *CPM1 PREMIUM BOT* 💀🚀\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ *ULTIMATE CPM COMMUNITY PANEL*\n\n"
        "Welcome, Player! Choose a menu below.\n"
        "💎 Premium interface • Fast navigation\n"
        "🛡️ Account safety first"
        + DISCLAIMER
    )
    await update.effective_message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard())

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛡️ *SAFETY CENTER*\n\n"
        "• Құпиясөз, email растау коды немесе 2FA/SMS кодын ешкімге жіберме.\n"
        "• Бот CPM серверіне ресми API арқылы қосылмаған.\n"
        "• Үшінші тараптың «аккаунт клондау» қызметтерінен сақ бол.\n"
        "• Сауда үшін сайттағы сатушыны мұқият тексер."
    )
    await update.effective_message.reply_text(text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ MENU", callback_data="home")]]))

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        f"🛒 *CPM MARKETPLACE*\nАккаунттар мен ойын ішіндегі заттарға арналған қауымдастық каталогы:\n{SITE_URL}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 OPEN MARKETPLACE", url=SITE_URL)]]))

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ADMIN_IDS:
        await update.effective_message.reply_text("⛔ Бұл команда тек әкімшіге арналған.")
        return
    await update.effective_message.reply_text(
        f"🛡️ *ADMIN PANEL*\n\nYour Telegram ID: `{user.id}`\nBot status: online\nMarketplace: {SITE_URL}\n\n"
        "Бұл бастапқы нұсқада әкімші мәзірі статус көрсетеді. Қосымша модерация API кейін байланыстырылады.",
        parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "home":
        await query.edit_message_text(
            "🚀 *CPM1 PREMIUM BOT* 💀🚀\n━━━━━━━━━━━━━━━━━━━━\nChoose your menu below." + DISCLAIMER,
            parse_mode="Markdown", reply_markup=main_keyboard())
    elif data.startswith("menu:"):
        key = data.split(":", 1)[1]
        title, _ = MENU[key]
        await query.edit_message_text(
            f"🚀 *CPM1 PREMIUM BOT*\n━━━━━━━━━━━━━━━━━━━━\n*{title}*\nChoose an option below.",
            parse_mode="Markdown", reply_markup=section_keyboard(key))
    elif data == "market":
        await query.edit_message_text(
            f"🛒 *CPM MARKETPLACE*\nBrowse community listings here:\n{SITE_URL}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 OPEN MARKETPLACE", url=SITE_URL)],
                [InlineKeyboardButton("⬅️ BACK", callback_data="home")]
            ]))
    elif data == "help":
        await query.edit_message_text(
            "🛡️ *SAFETY CENTER*\n\nNever share passwords, email codes, or 2FA/SMS codes. This bot does not modify game data.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ BACK", callback_data="home")]]))
    elif data in SAFE_TEXT:
        await query.edit_message_text(
            SAFE_TEXT[data] + "\n\n━━━━━━━━━━━━━━━━━━━━",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ BACK TO MAIN MENU", callback_data="home")]]))
    else:
        await query.edit_message_text("Бұл бөлім әзірге қолжетімсіз.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ MENU", callback_data="home")]]))

def main():
    if not BOT_TOKEN or BOT_TOKEN == "put_your_botfather_token_here":
        raise SystemExit("BOT_TOKEN-ды .env немесе хостинг Environment Variables ішіне енгізіңіз.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("catalog", catalog))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button_handler))
    log.info("CPM1 Premium Bot is starting")
    app.run_polling()

if __name__ == "__main__":
    main()
