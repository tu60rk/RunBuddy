import json
from pathlib import Path

class I18n:
    def __init__(self, default_lang="ru"):
        self.default_lang = default_lang
        self.locales = {}

    def load(self):
        for file in Path("locales").glob("*.json"):
            self.locales[file.stem] = json.loads(
                file.read_text(encoding="utf-8")
            )

    def t(self, key: str, lang: str):
        return (
            self.locales.get(lang, {}).get(key)
            or self.locales[self.default_lang].get(key)
            or key
        )

i18n = I18n()
i18n.load()