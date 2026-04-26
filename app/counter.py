from app.models import Champion, TeamComp

"""
Analyze how good a candidate is into the enemy team.
"""
def analyze_counter(candidate: Champion, enemy_team: TeamComp, champion_pool: dict[str, Champion]) -> dict[str, object]:

    selected = enemy_team.selected_champions()
    enemies = [champion_pool[name] for name in selected if name in champion_pool]

    score = 0.0
    breakdown = {}
    reasons = []

    anti_engage_score = 0.0
    anti_tank_score = 0.0
    anti_poke_score = 0.0
    anti_dive_score = 0.0
    punish_immobile_score = 0.0

    #Into engage-heavy teams: peel / mobility becomes valuable
    enemy_engage = sum(c.engage for c in enemies)
    if enemy_engage >= 12:
        if candidate.peel >= 6 or candidate.mobility >= 6:
            anti_engage_score = 3
            reasons.append(f"{candidate.name} can better survive or respond to heavy enemy engage.")

    #Into tanky teams: sustained damage or anti-frontline value
    enemy_durability = sum(c.durability for c in enemies)
    if enemy_durability >= 14:
        if candidate.teamfight >= 6 and candidate.damage_type in ["AD", "AP"]:
            anti_tank_score = 2
            reasons.append(f"{candidate.name} adds value against a durable enemy frontline.")

    #Into poke teams: engage / sustain / mobility helps
    enemy_poke_count = sum(1 for c in enemies if "poke" in c.tags)
    if enemy_poke_count >= 2:
        if candidate.engage >= 6 or candidate.mobility >= 6:
            anti_poke_score = 2
            reasons.append(f"{candidate.name} helps close distance against poke-oriented enemies.")

    #Into dive teams: peel and CC become more valuable
    enemy_dive_count = sum(1 for c in enemies if c.comp_scores.get("dive", 0) >= 2)
    if enemy_dive_count >= 2:
        if candidate.peel >= 6 or candidate.cc >= 6:
            anti_dive_score = 3
            reasons.append(f"{candidate.name} offers tools against enemy dive threats.")

    enemy_low_mobility_count = sum(1 for c in enemies if c.mobility <= 3)
    if enemy_low_mobility_count >= 2:
        if candidate.engage >= 7 or candidate.comp_scores.get("pick", 0) >= 2:
            punish_immobile_score = 2
            reasons.append(f"{candidate.name} can pressure immobile enemy champions effectively.")

    score = anti_engage_score + anti_tank_score + anti_poke_score + anti_dive_score + punish_immobile_score

    breakdown["anti_engage"] = anti_engage_score
    breakdown["anti_tank"] = anti_tank_score
    breakdown["anti_poke"] = anti_poke_score
    breakdown["anti_dive"] = anti_dive_score
    breakdown["punish_immobile"] = punish_immobile_score

    return {
        "score": score,
        "breakdown": breakdown,
        "reasons": reasons
    }