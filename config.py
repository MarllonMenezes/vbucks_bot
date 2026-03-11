"""
⚙️ config.py — Configurações do V-Bucks Alert Bot
Edite as variáveis abaixo conforme necessário.
"""

import os

# ── Token do Bot (obtido via @BotFather no Telegram) ──────────────────────────
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU TOKEN_AQUI")

# ── IDs dos chats que receberão alertas automáticos ───────────────────────────
# Deixe vazio [] para que os usuários se cadastrem via /start
# Ou preencha manualmente: CHAT_IDS = [123456789, 987654321]
_ids_env = os.getenv("TELEGRAM_CHAT_IDS", "")
CHAT_IDS: list[int] = [int(x) for x in _ids_env.split(",") if x.strip()] if _ids_env else []

# ── Intervalo de verificação automática (em minutos) ─────────────────────────
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL", "30"))

# ── URLs do site monitorado ───────────────────────────────────────────────────
BASE_URL = "https://freethevbucks.com"
MISSIONS_URL = f"{BASE_URL}/timed-missions/"

# ── User-Agent para as requisições HTTP ──────────────────────────────────────
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
