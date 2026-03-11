"""
🚀 main.py — Ponto de entrada do V-Bucks Alert Bot.
Execute: python main.py
"""

import logging
from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import config
from commands import cmd_start, cmd_status, cmd_stop, msg_bloqueada
from scheduler import start_scheduler

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


async def set_commands(app: Application) -> None:
    """Define os comandos visíveis no menu do Telegram (sem /start)."""
    await app.bot.set_my_commands([
        BotCommand("status", "💰 Ver V-Bucks disponíveis agora"),
        BotCommand("stop",   "🔕 Parar alertas"),
    ])
    log.info("✅ Comandos do menu configurados.")


def main() -> None:
    if config.BOT_TOKEN == "SEU_TOKEN_AQUI":
        print(
            "\n⚠️  Token não configurado!\n"
            "   Abra o arquivo config.py e substitua SEU_TOKEN_AQUI\n"
            "   pelo token gerado no @BotFather do Telegram.\n"
        )
        return

    log.info("🚀 Iniciando V-Bucks Alert Bot...")

    app = Application.builder().token(config.BOT_TOKEN).post_init(set_commands).build()

    # Comandos
    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("stop",   cmd_stop))

    # Bloqueia qualquer outra mensagem
    app.add_handler(MessageHandler(filters.ALL, msg_bloqueada))

    start_scheduler(app.bot)

    log.info("✅ Bot rodando! Pressione Ctrl+C para parar.")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
