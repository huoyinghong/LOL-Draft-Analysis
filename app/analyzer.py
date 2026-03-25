from app.models import TeamComp, Champion


def analyze_team_comp(team: TeamComp, champion_pool: dict[str, Champion]) -> dict:
    selected = team.selected_champions()
    champs = [champion_pool[name] for name in selected if name in champion_pool]

    if not champs:
        return {
            "ad": 0,
            "ap": 0,
            "cc": 0,
            "engage": 0,
            "peel": 0,
            "durability": 0,
            "split_push": 0,
            "teamfight": 0
        }

    ad = sum(1 for c in champs if c.damage_type == "AD")
    ap = sum(1 for c in champs if c.damage_type == "AP")
    mixed = sum(1 for c in champs if c.damage_type == "Mixed")

    return {
        "ad": ad + mixed * 0.5,
        "ap": ap + mixed * 0.5,
        "cc": sum(c.cc for c in champs) / len(champs),
        "engage": sum(c.engage for c in champs) / len(champs),
        "peel": sum(c.peel for c in champs) / len(champs),
        "durability": sum(c.durability for c in champs) / len(champs),
        "split_push": sum(c.split_push for c in champs) / len(champs),
        "teamfight": sum(c.teamfight for c in champs) / len(champs)
    }