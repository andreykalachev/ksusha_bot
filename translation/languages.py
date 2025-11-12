from enum import Enum


class Locale(str, Enum):
    RU = 'ru'
    EN = 'en'


class Language(str, Enum):
    ENGLISH = 'English'
    RUSSIAN = 'Русский'


LOCALE = 'locale'