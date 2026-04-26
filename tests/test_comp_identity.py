from app.comp_identity import analyze_comp_identity


def test_analyze_comp_identity_scores_main_ally_team(ally_team, champion_pool):
    result = analyze_comp_identity(ally_team, champion_pool)

    assert result["scores"] == {
        "front_to_back": 10,
        "dive": 4,
        "poke": 2,
        "pick": 4,
        "split_push": 0,
        "scaling": 9,
    }
    assert result["primary"] == "front_to_back"
    assert result["secondary"] == "scaling"
    assert result["summary"] == [
        "Primary identity: front_to_back",
        "Secondary identity: scaling",
        "This team is suited for structured front-to-back teamfights.",
        "This team has good late-game scaling.",
    ]
