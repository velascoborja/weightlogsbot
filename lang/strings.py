from strings_en import STRINGS as STRINGS_EN
from strings_es import STRINGS as STRINGS_ES

LANG_MAP = {
    "en": STRINGS_EN,
    "es": STRINGS_ES,
}

def get_strings(lang_code):
    lang = (lang_code or "en")[:2]
    return LANG_MAP.get(lang, STRINGS_EN) 