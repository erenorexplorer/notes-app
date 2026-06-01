from app.llm import service as llm_service
from app.vault import service as vault_service
# ====== File Notes ======
#
# - Orchestrator for cross-module functionalities
# - May later be split into separate files and given their own directory
#
# ========================


def create_formatted_draft(r_notes:str) -> dict:
    """Workflow:
        - have vault save raw and return uuid
        - get formatted from llm service
        - return formatted note and id to api"""
    uid = vault_service.create_raw_note(r_notes)
    formatted = llm_service.format_note(r_notes)
    result = {"id": uid, "Content": formatted}
    return result

def create_link_suggestions(uid:str, approved_note: str) -> dict:
    """Workflow:
        - update note status to approved in vault
        - later: get suggested links from llm service"""
    result = {"id": "OK", "Content": "content"}
    return result