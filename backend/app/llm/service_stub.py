from app.schemas import NoteOverview, LinkSuggestion

def format_note(raw: str) -> str:
    return "Placeholder Formatted Note.\nOriginal Note:\n" + raw

def suggest_links(approved_note: str, candidates: list[NoteOverview]) -> list[LinkSuggestion]:
    links = []
    for num, candidate in enumerate(candidates):
        if num % 2 == 0:
            links.append(LinkSuggestion(
                candidate_id=candidate.id,
                relation_type="related"
            ))

    return links[:5]