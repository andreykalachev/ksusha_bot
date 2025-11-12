from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime, timezone
from statistics.page_visits import PageVisits


def _time_now_str() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class StatisticsModel:
    bot_starts: int = 0
    page_visits: PageVisits = field(default_factory=PageVisits)
    last_reset: str = ""

    def reset(self) -> None:
        self.bot_starts = 0
        self.page_visits = PageVisits()
        self.last_reset = _time_now_str()

    def to_dict(self) -> Dict[str, object]:
        return {
            "bot_starts": self.bot_starts,
            "page_visits": self.page_visits.to_dict(),
            "last_reset": self.last_reset,
        }

    @staticmethod
    def from_dict(data: Dict[str, object]) -> "StatisticsModel":
        model = StatisticsModel(
            bot_starts=int(data.get("bot_starts", 0)),
            page_visits=PageVisits.from_dict(
                data.get("page_visits", {}) if isinstance(data.get("page_visits"), dict) else {}
            ),
            last_reset=str(data.get("last_reset", "")),
        )
        if not model.last_reset:
            model.last_reset = _time_now_str()
        return model
