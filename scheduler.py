"""
⏱️ scheduler.py — Verificação periódica de V-Bucks.
Roda em thread separada e envia alertas quando há V-Bucks disponíveis hoje.
"""

import asyncio
import logging
import time
import threading
import schedule
from telegram import Bot

import config
from scraper import fetch_vbucks_data
from formatter import format_status_message

log = logging.getLogger(__name__)

# Último valor notificado (evita spam)
_last_notified: int | None = None


async def _check_and_notify(bot: Bot) -> None:
    global _last_notified

    data = fetch_vbucks_data()
    if not data:
        return

    hoje = data.get("hoje", 0)

    if hoje > 0 and hoje != _last_notified:
        log.info("🚨 V-Bucks disponíveis hoje: %d — enviando alerta!", hoje)
        msg = format_status_message(data, is_alert=True)
        for chat_id in config.CHAT_IDS:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=False,
                )
                log.info("📨 Alerta enviado para chat %d", chat_id)
            except Exception as e:
                log.error("Erro ao enviar para %d: %s", chat_id, e)
        _last_notified = hoje

    elif hoje == 0:
        log.info("Sem V-Bucks hoje. Próxima verificação em %d min.", config.CHECK_INTERVAL_MINUTES)
        _last_notified = 0
    else:
        log.info("V-Bucks já notificados (%d). Sem mudança.", hoje)


def _run_loop(bot: Bot) -> None:
    """Loop do scheduler rodando em thread separada."""

    def job():
        asyncio.run(_check_and_notify(bot))

    schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(job)
    log.info("⏱️ Scheduler iniciado — verificação a cada %d min.", config.CHECK_INTERVAL_MINUTES)

    # Roda uma vez imediatamente ao iniciar
    job()

    while True:
        schedule.run_pending()
        time.sleep(10)


def start_scheduler(bot: Bot) -> None:
    """Inicia o scheduler em background (thread daemon)."""
    t = threading.Thread(target=_run_loop, args=(bot,), daemon=True)
    t.start()
