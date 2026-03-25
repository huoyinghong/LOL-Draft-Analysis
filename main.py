from app.models import TeamComp, DraftState
from app.data_loader import load_champions
from app.recommender import recommend_champions


def main():
    champion_pool = load_champions()

    ally_team = TeamComp(
        top="Ornn",
        jungle="Vi",
        mid="",
        adc="Jinx",
        support="Lulu"
    )

    enemy_team = TeamComp(
        top="Fiora",
        jungle="Vi",
        mid="Zed",
        adc="Jinx",
        support="Nautilus"
    )

    draft_state = DraftState(
        ally_team=ally_team,
        enemy_team=enemy_team,
        pick_role="mid"
    )

    recommendations = recommend_champions(draft_state, champion_pool, top_n=3)

    print("=== Recommended Champions ===")
    for i, rec in enumerate(recommendations, start=1):
        print(f"{i}. {rec.champion_name} - Score: {rec.total_score}")
        for reason in rec.reasons[:3]:
            print(f"   - {reason}")


if __name__ == "__main__":
    main()