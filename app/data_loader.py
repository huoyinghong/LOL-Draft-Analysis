import json
from pathlib import Path
from app.models import Champion


def load_champions(file_path: str = "data/champions.json") -> dict[str, Champion]:
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    champions = {}
    for item in raw_data:
        champion = Champion(**item)
        champions[champion.name] = champion

    return champions