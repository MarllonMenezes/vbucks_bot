"""
💬 formatter.py — Formata as mensagens enviadas pelo bot no Telegram.
"""

from config import MISSIONS_URL


def escape_md(text: str) -> str:
    """Escapa caracteres especiais do MarkdownV2."""
    chars = r"\_*[]()~`>#+-=|{}.!"
    for c in chars:
        text = text.replace(c, f"\\{c}")
    return text


def format_status_message(data: dict, is_alert: bool = False) -> str:
    hoje    = data.get("hoje", 0)
    ontem   = data.get("ontem", 0)
    s7d     = data.get("ultimos_7_dias", 0)
    s30d    = data.get("ultimos_30_dias", 0)
    aviso   = data.get("aviso", "")
    missoes = data.get("missoes", [])
    hora    = data.get("hora_verificacao", "")
    url     = data.get("url", MISSIONS_URL)

    header = "🚨 *ALERTA DE V\\-BUCKS\\!*\n\n" if is_alert else ""
    hoje_emoji = "✅" if hoje > 0 else "❌"

    msg = (
        f"{header}"
        f"🎮 *V\\-Bucks Grátis — Salve o Mundo*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{hoje_emoji} *Hoje:* {hoje} V\\-Bucks\n"
        f"📅 *Ontem:* {ontem} V\\-Bucks\n"
        f"📊 *Últimos 7 dias:* {s7d} V\\-Bucks\n"
        f"📆 *Últimos 30 dias:* {s30d} V\\-Bucks\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )

    if aviso:
        msg += f"⚠️ _{escape_md(aviso)}_\n━━━━━━━━━━━━━━━━━━━━\n"

    if missoes:
        msg += "🗺️ *Missões com V\\-Bucks:*\n"
        for m in missoes[:5]:
            msg += f"  • {escape_md(m)}\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"

    msg += (
        f"🔗 [Ver missões completas]({url})\n"
        f"🕐 Verificado em: {escape_md(hora)}"
    )
    return msg


def format_welcome_message(interval: int) -> str:
    return (
        "🎮 *V\\-Bucks Alert Bot ativado\\!*\n\n"
        "Você receberá alertas automáticos quando houver V\\-Bucks grátis "
        "disponíveis no Salve o Mundo do Fortnite\\.\n\n"
        "📌 *Comandos disponíveis:*\n"
        "/status — Ver V\\-Bucks agora\n"
        "/stop — Parar alertas"
    )
