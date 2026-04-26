from app.counter import analyze_counter


def test_analyze_counter_scores_candidate_against_enemy_team(enemy_team, champion_pool):
    result = analyze_counter(champion_pool["Galio"], enemy_team, champion_pool)

    assert result["score"] == 8.0
    assert result["breakdown"] == {
        "anti_engage": 3,
        "anti_tank": 2,
        "anti_poke": 0.0,
        "anti_dive": 3,
        "punish_immobile": 0.0,
    }
    assert result["reasons"] == [
        "Galio can better survive or respond to heavy enemy engage.",
        "Galio adds value against a durable enemy frontline.",
        "Galio offers tools against enemy dive threats.",
    ]
