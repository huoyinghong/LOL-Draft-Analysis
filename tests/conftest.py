import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data_loader import load_champions
from app.models import DraftState, TeamComp


@pytest.fixture
def champion_pool():
    return load_champions()


@pytest.fixture
def ally_team():
    return TeamComp(
        top="Ornn",
        jungle="Vi",
        mid="",
        adc="Jinx",
        support="Lulu",
    )


@pytest.fixture
def enemy_team():
    return TeamComp(
        top="Fiora",
        jungle="Vi",
        mid="Zed",
        adc="Jinx",
        support="Nautilus",
    )


@pytest.fixture
def draft_state(ally_team, enemy_team):
    return DraftState(
        ally_team=ally_team,
        enemy_team=enemy_team,
        pick_role="mid",
    )
