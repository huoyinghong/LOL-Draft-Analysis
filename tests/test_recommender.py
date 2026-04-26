from pytest import approx

from app.recommender import recommend_champions


def test_recommend_champions_returns_expected_mid_recommendations(draft_state, champion_pool):
    recommendations = recommend_champions(draft_state, champion_pool, top_n=3)

    assert [rec.champion_name for rec in recommendations] == [
        "Galio",
        "Orianna",
        "Ahri",
    ]
    assert [rec.total_score for rec in recommendations] == [
        44.8,
        38.27,
        26.38,
    ]
    assert recommendations[0].score_breakdown == {
        "engage_fit": approx(10.8),
        "cc_fit": 5.0,
        "durability_fit": 4.0,
        "teamfight_fit": 0.0,
        "damage_balance": 3,
        "anti_engage": 0,
        "identity_fit": 7,
        "synergy": 7.0,
        "counter": 8.0,
    }
    assert recommendations[0].reasons == [
        "Galio helps solve the team's engage problem because the current ally team lacks reliable initiation.",
        "Galio adds useful crowd control, which makes teamfights and picks easier to execute.",
        "Galio improves the team's frontline because the current composition is relatively squishy.",
        "Galio fits the team's main identity: front_to_back, while also supporting the secondary identity: scaling.",
        "Galio has good synergy with the existing ally champions.",
        "Galio has useful tools against the enemy team's current composition.",
    ]
