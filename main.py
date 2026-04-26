from app.models import TeamComp, DraftState
from app.data_loader import load_champions
from app.recommender import recommend_champions
from app.display import display


def main():
    champion_pool = load_champions()

    ally_team = TeamComp(
        top="Jayce",
        jungle="",
        mid="Ahri",
        adc="Ezreal",
        support="Lulu"
    )

    enemy_team = TeamComp(
        top="Fiora",
        jungle="Jarvan IV",
        mid="Zed",
        adc="Jinx",
        support="Nautilus"
    )
    draft_state = DraftState(
        ally_team=ally_team,
        enemy_team=enemy_team,
        pick_role="jungle"
    )
    #Create team drafts
    recommendations = recommend_champions(draft_state, champion_pool, top_n=3)

    display(recommendations, ally_team, enemy_team, champion_pool, draft_state)
    #Display result

if __name__ == "__main__":
    main()
