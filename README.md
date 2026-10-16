# 🚀 CPM1 PREMIUM BOT — Telegram starter

Бұл телефоннан орнатуға болатын Telegram боттың бастапқы жобасы. Интерфейс premium gaming стилінде, inline батырмалармен жұмыс істейді.

## Қазір не істейді?
- /start — premium басты мәзір
- Economy, Premium Features, Chrome, Car Unlock, Vinyl Tools, Car Copy, Account Settings, Siren, Bumper мәзірлері
- Батырма басылғанда түсіндірме және қолжетімді қауіпсіз әрекеттер көрсетіледі
- /catalog — CPM Marketplace веб-сайтына сілтеме
- /help — қауіпсіздік ережелері
- Әкімшіге арналған /admin командасы (ADMIN_IDS ішінде Telegram user ID көрсету керек)

## Маңызды шектеу
Бұл жоба CPM ойынының ішкі деректерін өзгертпейді. Money/coins орнату, көліктерді бұғаттан шығару, аккаунтты клондау, email/password ауыстыру сияқты ойын ішіндегі әрекеттер ойынның ресми API/рұқсат етілген интеграциясы болғанда ғана іске аса алады. Бұл шаблон оларды нақты орындамайды. Құпиясөз, 2FA/SMS коды немесе аккаунт токендерін сұрамайды.

## Телефонмен іске қосу
1. Telegram-да @BotFather ашып, `/newbot` командасымен бот жаса.
2. BotFather берген токенді көшір.
3. GitHub аккаунтыңды телефон браузерінен ашып, жаңа private repository жаса.
4. Осы архивтегі файлдарды repository-ге жүкте.
5. Render.com сайтына кіріп, GitHub-ты қос та, New > Background Worker таңда.
6. Build command: `pip install -r requirements.txt`
7. Start command: `python bot.py`
8. Environment variables:
   - `BOT_TOKEN` = BotFather токені
   - `PUBLIC_BASE_URL` = сайтыңның URL-і (болмаса `https://example.com`)
   - `ADMIN_IDS` = өз Telegram numeric user ID-ің (қажет болса, үтірмен бөл)
9. Deploy жаса, Telegram-да ботты `/start` арқылы тексер.

Токенді ешқашан чатқа, скриншотқа немесе ашық GitHub репозиторийге салма.

## Файлдар
- `bot.py` — боттың барлық мәзірлері
- `requirements.txt` — кітапханалар
- `.env.example` — локал ортаға үлгі
- `render.yaml` — Render Background Worker конфигурациясы
