from typing import Dict
from pathlib import Path
import yaml
from telegram.ext import ContextTypes
from pages import common

_cache: Dict[str, Dict[str, str]] = {}

# Exported keys
ABOUT_TEXT = 'ABOUT_TEXT'
LABEL_SERVICES = 'LABEL_SERVICES'
LABEL_PAINTINGS = 'LABEL_PAINTINGS'
LABEL_ARTICLES = 'LABEL_ARTICLES'
LABEL_BACK = 'LABEL_BACK'
LABEL_QUIZ = 'LABEL_QUIZ'
LABEL_GUIDE = 'LABEL_GUIDE'
LABEL_MAIN_MENU = 'LABEL_MAIN_MENU'
SERVICES_TEXT = 'SERVICES_TEXT'
PAINTINGS_TEXT = 'PAINTINGS_TEXT'
GUIDE_GREET = 'GUIDE_GREET'
GUIDE_TEXT = 'GUIDE_TEXT'
LABEL_CONTACTS = 'LABEL_CONTACTS'
CONTACTS_TEXT = 'CONTACTS_TEXT'
CONTACTS_BTN_TELEGRAM = 'CONTACTS_BTN_TELEGRAM'
CONTACTS_BTN_CHANNEL = 'CONTACTS_BTN_CHANNEL'
CONTACTS_BTN_INSTAGRAM = 'CONTACTS_BTN_INSTAGRAM'
CONTACTS_BTN_BEHANCE = 'CONTACTS_BTN_BEHANCE'
CONTACTS_BTN_EMAIL = 'CONTACTS_BTN_EMAIL'
ARTICLES_MENU_GREETING = 'ARTICLES_MENU_GREETING'


def _load_locale(locale: str) -> Dict[str, str]:
    if locale in _cache:
        return _cache[locale]
    base = Path(__file__).parent
    # prefer YAML files for human-friendly multiline support
    yaml_path = base / f"translations.{locale}.yaml"
    if yaml_path.exists():
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        _cache[locale] = data
        return data

    # final fallback: Russian YAML
    ru_yaml = base / 'translations.ru.yaml'
    if ru_yaml.exists():
        with open(ru_yaml, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        _cache[locale] = data
        return data

    _cache[locale] = {}
    return {}


def load(key: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    locale = common.get_locale(context)
    data = _load_locale(locale)
    return data.get(key, key)
