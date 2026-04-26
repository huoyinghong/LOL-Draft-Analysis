from app.synergy import analyze_synergy


def test_analyze_synergy_scores_candidate_against_ally_team(ally_team, champion_pool):
    result = analyze_synergy(champion_pool["Galio"], ally_team, champion_pool)

    assert result["score"] == 7.0
    assert result["breakdown"] == {
        "engage_followup": 3,
        "front_back": 2,
        "poke": 0.0,
        "protect": 2,
        "dive": 0.0,
    }
    assert result["reasons"] == [
        "Galio can follow strong engage and teamfight setups well.",
        "Galio benefits from having frontline support in structured fights.",
        "Galio works well with allies that can protect carries.",
    ]
