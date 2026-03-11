"""
🔍 scraper.py — Faz scraping do freethevbucks.com
Retorna os dados de V-Bucks disponíveis hoje e as missões ativas.
"""

import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import MISSIONS_URL, REQUEST_HEADERS

log = logging.getLogger(__name__)


def fetch_vbucks_data() -> dict:
    """
    Acessa freethevbucks.com/timed-missions/ e extrai:
      - hoje, ontem, ultimos_7_dias, ultimos_30_dias (int)
      - missoes: lista de strings com as missões que dão V-Bucks
      - aviso: texto de evento especial (se houver)
      - url, hora_verificacao
    Retorna {} em caso de erro.
    """
    try:
        resp = requests.get(MISSIONS_URL, headers=REQUEST_HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        log.error("Erro ao acessar o site: %s", e)
        return {}

    soup = BeautifulSoup(resp.text, "html.parser")

    data: dict = {
        "hoje": 0,
        "ontem": 0,
        "ultimos_7_dias": 0,
        "ultimos_30_dias": 0,
        "missoes": [],
        "aviso": "",
        "url": MISSIONS_URL,
        "hora_verificacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }

    # ── Extrai contadores TODAY / YESTERDAY / LAST 7 DAYS / LAST 30 DAYS ─────
    all_text = soup.get_text(separator="\n")
    lines = [l.strip() for l in all_text.splitlines() if l.strip()]

    labels = {
        "hoje":           ["today"],
        "ontem":          ["yesterday"],
        "ultimos_7_dias": ["last 7 days"],
        "ultimos_30_dias":["last 30 days"],
    }

    for i, line in enumerate(lines):
        low = line.lower()
        for key, keywords in labels.items():
            if any(kw in low for kw in keywords):
                for j in range(i + 1, min(i + 5, len(lines))):
                    candidate = (
                        lines[j]
                        .replace(",", "")
                        .replace(".", "")
                        .split("%")[0]
                        .split("+")[0]
                        .split("-")[0]
                        .strip()
                    )
                    if candidate.isdigit():
                        data[key] = int(candidate)
                        break

    # ── Aviso de evento especial ──────────────────────────────────────────────
    aviso_el = soup.find(string=lambda t: t and (
        "season" in t.lower() or "event" in t.lower() or "mini-boss" in t.lower()
    ))
    if aviso_el:
        data["aviso"] = aviso_el.strip()[:200]

    # ── Missões com V-Bucks ───────────────────────────────────────────────────
    mission_cards = soup.select(
        ".mission, .timed-mission, [class*='mission'], tr, .card"
    )
    for card in mission_cards[:20]:
        text = card.get_text(separator=" ").strip()
        if not text or len(text) < 5:
            continue
        if "v-buck" in text.lower() or "vbuck" in text.lower():
            data["missoes"].append(text[:120])

    log.info(
        "Scraping OK → Hoje: %d | Ontem: %d | 7d: %d | 30d: %d | Missões: %d",
        data["hoje"], data["ontem"],
        data["ultimos_7_dias"], data["ultimos_30_dias"],
        len(data["missoes"]),
    )
    return data
