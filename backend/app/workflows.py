from app.dependencies import get_llm_service
from app.vault import service as vault_service
from app.schemas import LinkSuggestion, LinkSuggestionForReview
# ====== File Notes ======
#
# - Orchestrator for cross-module functionalities
# - May later be split into separate files and given their own directory
#
# ========================
llm_service = get_llm_service()

def create_formatted_draft(title: str, raw_note: str) -> dict:
    """Workflow:
        - have vault save raw and return uuid
        - get formatted from llm service
        - return formatted note and id to api"""
    uid = vault_service.create_raw_note(raw_note)
    formatted = llm_service.format_note(raw_note)
    # title is redundant pass for now, may later include it in input to llm for cleaning + other metadata
    result = {"id": uid, "title": title, "content": formatted}
    return result

def create_link_suggestions(uid:str, title: str, approved_note: str) -> list[LinkSuggestionForReview]:
    """Workflow:
        - update note status to approved in vault
        - later: get suggested links from llm service"""
    # save approved note
    # dev note: currently directly saves user-entered title, future feature should add LLM suggestion.
    vault_service.save_approved_note(uid, title, approved_note)
    
    # create link suggestions
    candidates = vault_service.get_note_overviews()

    # temporary self-link prevention guard
    candidates = [
        candidate for candidate in candidates
        if candidate.id != uid
    ]

    suggestions = llm_service.suggest_links(approved_note, candidates)

    candidate_by_id = {
        candidate.id: candidate
        for candidate in candidates
    }

    result = [
        LinkSuggestionForReview(
            candidate_id=suggestion.candidate_id,
            candidate_title=candidate_by_id[suggestion.candidate_id].title,
            relation_type=suggestion.relation_type,
        )
        for suggestion in suggestions
    ]

    return result

def approve_links(uid:str, approved_links: list[LinkSuggestion]):
    """Workflow:
        - save approved links to vault
        - later: trigger other actions like updating a graph or sending notifications"""
    vault_service.save_approved_links(uid, approved_links)