from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from enum import Enum


class Page(Enum):
    MAIN = "main"
    GUIDE = "guide"
    QUIZ = "quiz"
    CONTACTS = "contacts"
    PAINTINGS = "paintings"
    SERVICES = "services"


@dataclass
class PageVisits:
    main: int = 0
    guide: int = 0
    quiz: int = 0
    contacts: int = 0
    paintings: int = 0
    services: int = 0

    def increment(self, page: Page) -> None:
        if page is Page.MAIN:
            self.main += 1
        elif page is Page.GUIDE:
            self.guide += 1
        elif page is Page.QUIZ:
            self.quiz += 1
        elif page is Page.CONTACTS:
            self.contacts += 1
        elif page is Page.PAINTINGS:
            self.paintings += 1
        elif page is Page.SERVICES:
            self.services += 1

    def to_dict(self) -> Dict[str, int]:
        return {
            "main": self.main,
            "guide": self.guide,
            "quiz": self.quiz,
            "contacts": self.contacts,
            "paintings": self.paintings,
            "services": self.services,
        }

    @staticmethod
    def from_dict(data: Dict[str, object]) -> "PageVisits":
        return PageVisits(
            main=int(data.get("main", 0)),
            guide=int(data.get("guide", 0)),
            quiz=int(data.get("quiz", 0)),
            contacts=int(data.get("contacts", 0)),
            paintings=int(data.get("paintings", 0)),
            services=int(data.get("services", 0)),
        )
