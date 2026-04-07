from app.models import DraftState, RecommendationResult
from app.scorer import score_candidate


def recommend_champions(draft_state: DraftState,champion_pool: dict,top_n: int = 3) -> list[RecommendationResult]:
    role = draft_state.pick_role#Current role need to be picked

    candidates = [
        champ for champ in champion_pool.values()
        if role in champ.roles and champ.name not in draft_state.ally_team.selected_champions()
    ]#Only consider champs match the role and hasnt been picked

    results = []
    for candidate in candidates:
        total_score, breakdown = score_candidate(candidate, draft_state, champion_pool)

        reasons = sorted(
            breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )

        readable_reasons = [f"{k}: {v:.2f}" for k, v in reasons if v > 0]

        results.append(
            RecommendationResult(
                champion_name=candidate.name,
                total_score=round(total_score, 2),
                reasons=readable_reasons,
                score_breakdown=breakdown
            )
        )

    results.sort(key=lambda x: x.total_score, reverse=True)
    return results[:top_n]