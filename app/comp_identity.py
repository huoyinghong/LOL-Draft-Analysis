from collections import defaultdict

from app.models import Champion, TeamComp


COMP_TYPES = [
    "front_to_back",
    "dive",
    "poke",
    "pick",
    "split_push",
    "scaling",
]


def analyze_comp_identity(team: TeamComp, champion_pool: dict[str, Champion]) -> dict[str, object]:
    """
    Analyze overall team composition identity based on selected champions' comp_scores.
    """
    selected = team.selected_champions()
    champs = [champion_pool[name] for name in selected if name in champion_pool]

    total_scores = defaultdict(int)

    for champion in champs:
        comp_scores = getattr(champion, "comp_scores", {}) or {}
        for comp_type in COMP_TYPES:
            total_scores[comp_type] += comp_scores.get(comp_type, 0)

    sorted_identities = sorted(
        total_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary = sorted_identities[0][0] if sorted_identities and sorted_identities[0][1] > 0 else None
    secondary = sorted_identities[1][0] if len(sorted_identities) > 1 and sorted_identities[1][1] > 0 else None

    summary = build_identity_summary(total_scores, primary, secondary)

    return {
        "scores": dict(total_scores),
        "primary": primary,
        "secondary": secondary,
        "summary": summary,
    }


def build_identity_summary(scores, primary, secondary):
    summary = []

    if primary:
        summary.append(f"Primary identity: {primary}")
    else:
        summary.append("Primary identity: unclear")

    if secondary:
        summary.append(f"Secondary identity: {secondary}")

    if scores.get("poke", 0) >= 6:
        summary.append("This team has strong poke potential before teamfights.")

    if scores.get("dive", 0) >= 6:
        summary.append("This team can strongly threaten enemy backline through dive.")

    if scores.get("front_to_back", 0) >= 6:
        summary.append("This team is suited for structured front-to-back teamfights.")

    if scores.get("pick", 0) >= 5:
        summary.append("This team has decent pick and catch potential.")

    if scores.get("split_push", 0) >= 5:
        summary.append("This team can create side-lane pressure.")

    if scores.get("scaling", 0) >= 5:
        summary.append("This team has good late-game scaling.")

    return summary
