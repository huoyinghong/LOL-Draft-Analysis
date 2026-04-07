from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Champion:
    name: str
    roles: List[str]
    damage_type: str
    tags: List[str]
    early_game: int
    mid_game: int
    late_game: int
    mobility: int
    cc: int
    durability: int
    engage: int
    peel: int
    split_push: int
    teamfight: int
    comp_scores: Dict[str, int]


@dataclass
class TeamComp:#Picked champs
    top: str = ""
    jungle: str = ""
    mid: str = ""
    adc: str = ""
    support: str = ""

    def selected_champions(self) -> List[str]:
        return [c for c in [self.top, self.jungle, self.mid, self.adc, self.support] if c]


@dataclass
class DraftState:
    ally_team: TeamComp
    enemy_team: TeamComp
    pick_role: str            #mid


@dataclass
class RecommendationResult:
    champion_name: str
    total_score: float
    reasons: List[str] = field(default_factory=list)
    score_breakdown: Dict[str, float] = field(default_factory=dict)