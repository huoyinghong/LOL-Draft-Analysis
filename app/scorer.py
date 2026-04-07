from app.models import Champion, DraftState
from app.analyzer import analyze_team_comp
from app.comp_identity import analyze_comp_identity
from app.synergy import analyze_synergy
from app.counter import analyze_counter


def score_candidate(candidate: Champion, draft_state: DraftState, champion_pool: dict[str, Champion]) -> tuple[float, dict]:
    ally_analysis = analyze_team_comp(draft_state.ally_team, champion_pool)
    enemy_analysis = analyze_team_comp(draft_state.enemy_team, champion_pool)
    ally_identity = analyze_comp_identity(draft_state.ally_team, champion_pool)
    primary_identity = ally_identity["primary"]
    secondary_identity = ally_identity["secondary"]

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

    #If team is too squishy -> higher score for champions with high durability
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


    #Bonus for candidates that match the ally team's primary or secondary comp identity.
    identity_score = 0
    if primary_identity:
        identity_score += candidate.comp_scores.get(primary_identity, 0) * 2

    if secondary_identity:
        identity_score += candidate.comp_scores.get(secondary_identity, 0) * 1

    score += identity_score
    breakdown["identity_fit"] = identity_score


    synergy_result = analyze_synergy(candidate, draft_state.ally_team, champion_pool)
    counter_result = analyze_counter(candidate, draft_state.enemy_team, champion_pool)

    score += synergy_result["score"]
    score += counter_result["score"]

    breakdown["synergy"] = synergy_result["score"]
    breakdown["counter"] = counter_result["score"]

    return score, breakdown