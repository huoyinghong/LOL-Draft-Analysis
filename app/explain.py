from app.models import Champion, DraftState
from app.analyzer import analyze_team_comp
from app.comp_identity import analyze_comp_identity


def explain_recommendation(candidate: Champion,draft_state: DraftState,
    champion_pool: dict[str, Champion],score_breakdown: dict[str, float]) -> list[str]:
    """
    Convert numeric score breakdown into human-readable explanation.
    """

    reasons = []

    ally_analysis = analyze_team_comp(draft_state.ally_team, champion_pool)
    enemy_analysis = analyze_team_comp(draft_state.enemy_team, champion_pool)
    ally_identity = analyze_comp_identity(draft_state.ally_team, champion_pool)

    primary_identity = ally_identity["primary"]
    secondary_identity = ally_identity["secondary"]

    if score_breakdown.get("engage_fit", 0) > 0:
        reasons.append(
            f"{candidate.name} helps solve the team's engage problem because the current ally team lacks reliable initiation."
        )

    if score_breakdown.get("cc_fit", 0) > 0:
        reasons.append(
            f"{candidate.name} adds useful crowd control, which makes teamfights and picks easier to execute."
        )

    if score_breakdown.get("durability_fit", 0) > 0:
        reasons.append(
            f"{candidate.name} improves the team's frontline because the current composition is relatively squishy."
        )

    if score_breakdown.get("teamfight_fit", 0) > 0:
        reasons.append(
            f"{candidate.name} strengthens the team's 5v5 teamfight potential."
        )

    if score_breakdown.get("damage_balance", 0) >= 8:
        reasons.append(
            f"{candidate.name} helps balance the team's damage type as a {candidate.damage_type} champion."
        )

    if score_breakdown.get("anti_engage", 0) > 0:
        reasons.append(
            f"{candidate.name} is valuable against the enemy team's engage because they can provide peel or counter-engage tools."
        )

    if score_breakdown.get("identity_fit", 0) > 0:
        if primary_identity and secondary_identity:
            reasons.append(
                f"{candidate.name} fits the team's main identity: {primary_identity}, while also supporting the secondary identity: {secondary_identity}."
            )
        elif primary_identity:
            reasons.append(
                f"{candidate.name} fits the team's main composition identity: {primary_identity}."
            )

    if score_breakdown.get("synergy", 0) > 0:
        reasons.append(
            f"{candidate.name} has good synergy with the existing ally champions."
        )

    if score_breakdown.get("counter", 0) > 0:
        reasons.append(
            f"{candidate.name} has useful tools against the enemy team's current composition."
        )

    if not reasons:
        reasons.append(
            f"{candidate.name} is a playable option, but does not strongly solve a major team need in this draft."
        )

    return reasons