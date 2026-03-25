from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Champion:
    name: str
    roles: List[str]
    damage_type: str          # "AD", "AP", "Mixed"
    tags: List[str]           # ["engage", "tank", "cc", "scaling"]
    early_game: int           # 1-10
    mid_game: int             # 1-10
    late_game: int            # 1-10
    mobility: int             # 1-10
    cc: int                   # 1-10
    durability: int           # 1-10
    engage: int               # 1-10
    peel: int                 # 1-10
    split_push: int           # 1-10
    teamfight: int            # 1-10


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