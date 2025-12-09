from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from enum import Enum


class Page(Enum):
    MAIN = "main"
    GUIDE = "guide"
    INSPIRATION = "inspiration"
    CONTACTS = "contacts"
    PAINTINGS = "paintings"
    SERVICES = "services"
    INFO = "info"
    REVIEWS = "reviews"
    MINI_SHOP = "mini_shop"


@dataclass
class PageVisits:
    main: int = 0
    guide: int = 0
    contacts: int = 0
    paintings: int = 0
    services: int = 0
    info: int = 0
    reviews: int = 0
    mini_shop: int = 0
    inspiration: int = 0

    def increment(self, page: Page) -> None:
        if page is Page.MAIN:
            self.main += 1
        elif page is Page.GUIDE:
            self.guide += 1
        elif page is Page.INSPIRATION:
            self.inspiration += 1
        elif page is Page.CONTACTS:
            self.contacts += 1
        elif page is Page.PAINTINGS:
            self.paintings += 1
        elif page is Page.SERVICES:
            self.services += 1
        elif page is Page.INFO:
            self.info += 1
        elif page is Page.REVIEWS:
            self.reviews += 1
        elif page is Page.MINI_SHOP:
            self.mini_shop += 1

    def to_dict(self) -> Dict[str, int]:
        return {
            "main": self.main,
            "guide": self.guide,
            "contacts": self.contacts,
            "paintings": self.paintings,
            "services": self.services,
            "info": self.info,
            "reviews": self.reviews,
            "mini_shop": self.mini_shop,
            "inspiration": self.inspiration,
        }

    @staticmethod
    def from_dict(data: Dict[str, object]) -> "PageVisits":
        return PageVisits(
            main=int(data.get("main", 0)),
            guide=int(data.get("guide", 0)),
            contacts=int(data.get("contacts", 0)),
            paintings=int(data.get("paintings", 0)),
            services=int(data.get("services", 0)),
            info=int(data.get("info", 0)),
            reviews=int(data.get("reviews", 0)),
            mini_shop=int(data.get("mini_shop", 0)),
            inspiration=int(data.get("inspiration", 0)),
        )
