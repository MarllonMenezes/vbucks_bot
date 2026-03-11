"""
📱 commands.py — Handlers dos comandos do Telegram.
/start, /status, /stop
Mensagens fora dos comandos são bloqueadas automaticamente.
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

import config
from scraper import fetch_vbucks_data
from formatter import format_status_message, format_welcome_message

log = logging.getLogger(__name__)

# ── Teclado fixo com os botões dos comandos ───────────────────────────────────
MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("/status")],
        [KeyboardButton("/stop")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in config.CHAT_IDS:
        config.CHAT_IDS.append(chat_id)
        log.info("✅ Chat %d cadastrado para alertas.", chat_id)
    await update.message.reply_text(
        format_welcome_message(config.CHECK_INTERVAL_MINUTES),
        parse_mode="MarkdownV2",
        reply_markup=MENU_KEYBOARD,
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔍 Verificando V\-Bucks\.\.\. aguarde\.", parse_mode="MarkdownV2")
    data = fetch_vbucks_data()
    if not data:
        await update.message.reply_text("❌ Não foi possível obter os dados\. Tente novamente mais tarde\.", parse_mode="MarkdownV2")
        return
    msg = format_status_message(data)
    await update.message.reply_text(msg, parse_mode="MarkdownV2", disable_web_page_preview=False)


async def cmd_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in config.CHAT_IDS:
        config.CHAT_IDS.remove(chat_id)
        log.info("🔕 Chat %d removido dos alertas.", chat_id)
        await update.message.reply_text("🔕 Alertas desativados\. Use /start para reativar\.", parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("Você já não está recebendo alertas\.", parse_mode="MarkdownV2")


async def msg_bloqueada(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bloqueia qualquer mensagem que não seja um comando reconhecido."""
    await update.message.reply_text(
        "⛔ *Comando inválido\!*\n\n"
        "Use apenas os comandos disponíveis:\n"
        "/status — Ver V\-Bucks agora\n"
        "/stop — Parar alertas\n\n"
        "Ou clique nos botões abaixo 👇",
        parse_mode="MarkdownV2",
        reply_markup=MENU_KEYBOARD,
    )
