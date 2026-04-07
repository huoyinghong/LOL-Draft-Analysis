from app.models import TeamComp, DraftState
from app.data_loader import load_champions
from app.recommender import recommend_champions
from app.comp_identity import analyze_comp_identity
from app.synergy import analyze_synergy
from app.counter import analyze_counter


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

    identity_result = analyze_comp_identity(ally_team, champion_pool)

    print("\n=== Ally Team Identity ===")
    print("Scores:", identity_result["scores"])
    print("Primary:", identity_result["primary"])
    print("Secondary:", identity_result["secondary"])
    for line in identity_result["summary"]:
        print("-", line)

    for i, rec in enumerate(recommendations, start=1):
        candidate = champion_pool[rec.champion_name]

        synergy_result = analyze_synergy(candidate, ally_team, champion_pool)
        counter_result = analyze_counter(candidate, enemy_team, champion_pool)

        print(f"\n=== Synergy Test {i}===")
        print("Candidate:", candidate.name)
        print("Score:", synergy_result["score"])
        print("Breakdown:", synergy_result["breakdown"])
        for reason in synergy_result["reasons"]:
            print("-", reason)

        print(f"\n=== Counter Test {i}===")
        print("Candidate:", candidate.name)
        print("Score:", counter_result["score"])
        print("Breakdown:", counter_result["breakdown"])
        for reason in counter_result["reasons"]:
            print("-", reason)

if __name__ == "__main__":
    main()