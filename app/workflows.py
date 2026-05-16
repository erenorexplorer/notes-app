import llm.service as llm_s
# ====== File Notes ======
#
# - Orchestrator for cross-module functionalities
# - May later be split into separate files and given their own directory
#
# ========================


# def raw_to_save(r_notes:str) -> dict:
#     """(E1) Pass raw notes to LLM module, return success and formatted version in dict"""
#     result = {"Status": "OK", "Content": llm_s.format_note(r_notes.content)}
#     return result
