import json
import os
import re

# Если скрипт лежит прямо в папке со статьями лора:
VAULT_DIR = "."
OUTPUT_FILE = "obsidian_world_lore.json"

entries = {}
uid = 0

for root, _, files in os.walk(VAULT_DIR):
    for file in files:
        if file.endswith(".md"):
            # Имя файла без расширения становится названием записи и главным триггером
            title = os.path.splitext(file)[0]
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            # Удаляем YAML frontmatter (служебные свойства Obsidian в начале заметки, если они есть)
            clean_text = re.sub(r"^---\n.*?\n---\n", "", raw_text, flags=re.DOTALL)

            # Очищаем вики-ссылки: [[Название|Алиас]] -> Алиас, [[Название]] -> Название
            clean_text = re.sub(r"\[\[.*?\|(.*?)\]\]", r"\1", clean_text)
            clean_text = re.sub(r"\[\[(.*?)\]\]", r"\1", clean_text)
            clean_text = clean_text.strip()

            if not clean_text:
                continue

            # Формируем список триггеров: само название и его варианты
            keys = [title.strip()]
            if title.lower() not in [k.lower() for k in keys]:
                keys.append(title.lower())

            # Структура карточки по спецификации SillyTavern World Info
            entries[str(uid)] = {
                "uid": uid,
                "key": keys,
                "keysecondary": [],
                "comment": title,
                "content": clean_text,
                "constant": False,
                "selective": True,
                "order": 100,
                "position": 0,
                "disable": False,
                "excludeRecursion": False,
                "preventRecursion": False,
                "delayUntilRecursion": False,
                "probability": 100,
                "useProbability": True,
                "depth": 4,
                "scanDepth": None,
                "caseSensitive": False,
                "matchWholeWords": None,
                "useGroup": False,
                "group": "",
                "groupOverride": False,
                "groupWeight": 100,
            }
            uid += 1

lorebook_data = {
    "entries": entries,
    "originalData": {
        "name": "Obsidian Lore",
        "description": "Импортированная база знаний мира",
        "scan_depth": 5,
        "token_budget": 2048,
        "recursive_scanning": True,
    },
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(lorebook_data, out, ensure_ascii=False, indent=2)

print(
    f"Готово! Создан файл {OUTPUT_FILE}, успешно сконвертировано записей: {uid}"
)