from app.comp_identity import analyze_comp_identity
from app.synergy import analyze_synergy
from app.counter import analyze_counter


def get_unselected_champions(ally_team, enemy_team, champion_pool, draft_state):
    selected = set(ally_team.selected_champions() + enemy_team.selected_champions())
    return [
        champion for champion in champion_pool.values()
        if champion.name not in selected and draft_state.pick_role in champion.roles
    ]


def display(recommendations, ally_team, enemy_team, champion_pool, draft_state, top_n=3):

    identity_result = analyze_comp_identity(ally_team, champion_pool)

    print("\n=== Ally Team Identity ===")
    print("Scores:", identity_result["scores"])
    print("Primary:", identity_result["primary"])
    print("Secondary:", identity_result["secondary"])
    for line in identity_result["summary"][2:]:
        print("-", line)

    unselected_champions = get_unselected_champions(
        ally_team,
        enemy_team,
        champion_pool,
        draft_state
    )
    synergy_results = []
    counter_results = []

    for candidate in unselected_champions:
        synergy_result = analyze_synergy(candidate, ally_team, champion_pool)
        counter_result = analyze_counter(candidate, enemy_team, champion_pool)
        synergy_results.append((candidate, synergy_result))
        counter_results.append((candidate, counter_result))

    synergy_results.sort(
        key=lambda item: (item[1]["score"], item[0].name),
        reverse=True,
    )
    counter_results.sort(
        key=lambda item: (item[1]["score"], item[0].name),
        reverse=True,
    )

    print("\n=== Synergy Recommendations ===")
    for i, (candidate, synergy_result) in enumerate(synergy_results[:top_n], start=1):
        print(f"\n{i}. {candidate.name}")
        print("Candidate:", candidate.name)
        print("Score:", synergy_result["score"])
        print("Breakdown:", synergy_result["breakdown"])
        for reason in synergy_result["reasons"]:
            print("-", reason)

    print("\n=== Counter Recommendations ===")
    for i, (candidate, counter_result) in enumerate(counter_results[:top_n], start=1):
        print(f"\n{i}. {candidate.name}")
        print("Candidate:", candidate.name)
        print("Score:", counter_result["score"])
        print("Breakdown:", counter_result["breakdown"])
        for reason in counter_result["reasons"]:
            print("-", reason)


    print("\n=== Overall Recommended Champions ===")
    for i, rec in enumerate(recommendations, start=1):
        print(f"\n{i}. {rec.champion_name} - Score: {rec.total_score}")

        print("Reasons:")
        for reason in rec.reasons[:5]:
            print(f"   - {reason}")

        print("Score Breakdown:")
        for key, value in rec.score_breakdown.items():
            print(f"   {key}: {value:.2f}")
