from app.models import Champion, TeamComp

"""
Analyze how well a candidate synergizes with the ally team.
"""
def analyze_synergy(candidate: Champion, ally_team: TeamComp, champion_pool: dict[str, Champion]) -> dict[str, object]:

    selected = ally_team.selected_champions()
    allies = [champion_pool[name] for name in selected if name in champion_pool]

    score = 0.0
    breakdown = {}
    reasons = []

    engage_followup_score = 0.0
    front_back_score = 0.0
    poke_score = 0.0
    protect_score = 0.0
    dive_score = 0.0

    #Engage + follow-up synergy
    ally_engage = sum(c.engage for c in allies)
    ally_cc = sum(c.cc for c in allies)
    if ally_engage >= 7 or ally_cc >= 10:
        if candidate.teamfight >= 7 or candidate.engage >= 6:
            engage_followup_score = 3
            reasons.append(f"{candidate.name} can follow strong engage and teamfight setups well.")

    #Frontline + backline synergy
    ally_frontline = sum(c.durability for c in allies)
    if ally_frontline >= 12 and candidate.damage_type in ["AD", "AP"] and candidate.teamfight >= 6:
        front_back_score = 2
        reasons.append(f"{candidate.name} benefits from having frontline support in structured fights.")

    #Poke synergy
    ally_poke_count = sum(1 for c in allies if "poke" in c.tags)
    if ally_poke_count >= 2 and "poke" in candidate.tags:
        poke_score = 3
        reasons.append(f"{candidate.name} strengthens an existing poke game plan.")

    #Peel synergy
    ally_peel = sum(c.peel for c in allies)
    if ally_peel >= 8 and candidate.teamfight >= 6:
        protect_score = 2
        reasons.append(f"{candidate.name} works well with allies that can protect carries.")

    #Dive synergy
    ally_dive_count = sum(1 for c in allies if c.comp_scores.get("dive", 0) >= 2)
    if ally_dive_count >= 2 and candidate.comp_scores.get("dive", 0) >= 2:
        dive_score = 3
        reasons.append(f"{candidate.name} fits an allied dive-oriented setup.")

    score = engage_followup_score + front_back_score + poke_score + protect_score + dive_score

    breakdown["engage_followup"] = engage_followup_score
    breakdown["front_back"] = front_back_score
    breakdown["poke"] = poke_score
    breakdown["protect"] = protect_score
    breakdown["dive"] = dive_score

    return {
        "score": score,
        "breakdown": breakdown,
        "reasons": reasons
    }