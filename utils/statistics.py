from __future__ import annotations

import json
from pathlib import Path
from statistics.statistics_model import StatisticsModel
from statistics.page_visits import Page


_STATS_FILE = Path(__file__).resolve().parent.parent / "statistics" / "data" / "stats.json"


def _ensure_file() -> None:
    _STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not _STATS_FILE.exists() or _STATS_FILE.stat().st_size == 0:
        model = StatisticsModel()
        model.reset()
        _STATS_FILE.write_text(json.dumps(model.to_dict(), indent=2), encoding="utf-8")


def _load() -> StatisticsModel:
    _ensure_file()
    with _STATS_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return StatisticsModel.from_dict(raw if isinstance(raw, dict) else {})


def _save(model: StatisticsModel) -> None:
    _STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _STATS_FILE.write_text(json.dumps(model.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")


# Load model once on import and keep it in memory. Write on every update.
_MODEL: StatisticsModel = _load()


def increment_bot_start() -> None:
    _MODEL.bot_starts += 1
    _MODEL.page_visits.increment(Page.MAIN)
    _save(_MODEL)


def increment_page(page: Page) -> None:
    _MODEL.page_visits.increment(page)
    _save(_MODEL)


def reset() -> StatisticsModel:
    _MODEL.reset()
    _save(_MODEL)
    return _MODEL


def format_model(model: StatisticsModel) -> str:
    pv = model.page_visits
    last_reset = model.last_reset if model.last_reset else "never"

    lines = [
        "Statistics:",
        f"• Main: {pv.main}",
        f"• Guide: {pv.guide}",
        f"• Contacts: {pv.contacts}",
        f"• Paintings: {pv.paintings}",
        f"• Services: {pv.services}",
        f"- Last reset: {last_reset}",
    ]
    return "\n".join(lines)


def get_stats_text() -> str:
    return format_model(_MODEL)
