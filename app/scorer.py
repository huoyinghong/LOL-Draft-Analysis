from app.models import Champion, DraftState
from app.analyzer import analyze_team_comp

#
def score_candidate(candidate: Champion, draft_state: DraftState, champion_pool: dict[str, Champion]) -> tuple[float, dict]:
    ally_analysis = analyze_team_comp(draft_state.ally_team, champion_pool)
    enemy_analysis = analyze_team_comp(draft_state.enemy_team, champion_pool)

    score = 0.0
    breakdown = {}

    #If team lacks engage ->  higher score for champions with strong engage
    engage_need = max(0, 7 - ally_analysis["engage"])
    engage_score = engage_need * candidate.engage * 0.6
    score += engage_score
    breakdown["engage_fit"] = engage_score

    # If team lacks crowd control -> higher score for champions with strong CC
    cc_need = max(0, 7 - ally_analysis["cc"])
    cc_score = cc_need * candidate.cc * 0.5
    score += cc_score
    breakdown["cc_fit"] = cc_score

    # 3. If team is too squishy -> higher score for champions with high durability
    tank_need = max(0, 6 - ally_analysis["durability"])
    durability_score = tank_need * candidate.durability * 0.5
    score += durability_score
    breakdown["durability_fit"] = durability_score

    #If team is weak in teamfights -> higher score for champions with strong teamfight ability
    tf_need = max(0, 7 - ally_analysis["teamfight"])
    tf_score = tf_need * candidate.teamfight * 0.4
    score += tf_score
    breakdown["teamfight_fit"] = tf_score

    #Damage type balance
    if ally_analysis["ad"] > ally_analysis["ap"] and candidate.damage_type == "AP":
        dmg_balance_score = 8
    elif ally_analysis["ap"] > ally_analysis["ad"] and candidate.damage_type == "AD":
        dmg_balance_score = 8
    else:
        dmg_balance_score = 3
    score += dmg_balance_score
    breakdown["damage_balance"] = dmg_balance_score

    #If  enemy team has strong engage -> extra score to champions with strong peel
    anti_engage_score = 0
    if enemy_analysis["engage"] >= 7:
        anti_engage_score = candidate.peel * 0.8
        score += anti_engage_score
    breakdown["anti_engage"] = anti_engage_score

    return score, breakdown