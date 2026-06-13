import json

from openai import OpenAI
from app.schemas import NoteOverview, LinkSuggestion

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

MODEL = "qwen3:4b-instruct"


def format_note(raw:str) -> str:
    """Call LLM to format raw note and return formatted note"""
    # chat-style API, completions instead of respoinse for older model compatability
    response = client.chat.completions.create(
        model=MODEL,
        messages = [
            {
                "role": "system",
                "content": (
                    "You format rough learning notes into clean Markdown. "
                    "Preserve meaning. Do not invent facts or add new information. Keep the result concise and reviewable."
                    "Prioritize human readability and scannability."
                ),
            },
            {
                "role": "user",
                "content": raw,
            },
        ],
    )
    
    return response.choices[0].message.content

LINK_SUGGESTION_SYSTEM_PROMPT = (
    "You suggest useful links between notes. "
    "Only choose from the provided candidate numbers. "
    "Return zero links if none are clearly useful. "
    "Do not invent candidate numbers."
)

# Specifies response format using OpenAI structure output
LINK_SUGGESTION_RESPONSE_FORMAT = {
    "type": "json_schema",                                                     # Use OpenAI's JSON Schema response mode
    "json_schema": {
        "name": "link_suggestions",                                            # name of the schema                               
        "strict": True,                                                        # response must match schema exactly              
        "schema": {
            "type": "object",                                                  # response is an object
            "properties": {
                "links": {                                                     # response has a 'links' property
                    "type": "array",                                              # 'links' is an array
                    "maxItems": 5,                                                # maximum of 5 links
                    
                    # shape of each object in 'links' array
                    "items": {
                        "type": "object",
                        "properties": {
                            "candidate_number": {"type": "integer"},
                            "relation_type": {
                                "type": "string",
                                "enum": ["related"],
                            },
                        },
                        "required": ["candidate_number", "relation_type"],        # mandatory fields      
                        "additionalProperties": False,                            # no extra fields allowed (per link suggestion)
                    },
                },
            },
            "required": ["links"],                                          # 'links' property is mandatory
            "additionalProperties": False,                                  # no extra fields allowed at the top level
        },
    },
}

def suggest_links(approved_note: str, candidates: list[NoteOverview]) -> list[LinkSuggestion]:
    """Call LLM to suggest links based on approved note and candidate notes"""
    # create numbered candidate list for LLM
    # feed approved_note + numbered candidates to LLM
    # parse output: candidate numbers + relation type
    # validate candidate numbers against numbered list
    # map candidate numbers back to real note UUIDs
    # package into list[LinkSuggestion]
    # return suggestions for user approval

    # indexed candidates for lookup
    indexed_link_candidates = {
        index: candidate 
        for index, candidate in enumerate(candidates, start=1)
    }

    # indexed candidates for LLM input
    input_candidates = [
        {
            "index": num,
            "title": candidate.title,
        }
        for num, candidate in indexed_link_candidates.items()
    ]

    llm_input = {
        "approved_note": approved_note,
        "candidates": input_candidates,
    }

    # send instructions to llm and get response
    response = client.chat.completions.create(
        model=MODEL,
        messages = [
            {
                "role": "system",
                "content": LINK_SUGGESTION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(llm_input, indent=2),
            }
        ],
        response_format=LINK_SUGGESTION_RESPONSE_FORMAT,
        temperature=0,
    )

    answer = response.choices[0].message.content
    # Answer Data Shape:
    # {
    # "links": [
    #        {
    #            "candidate_number": 1,
    #            "relation_type": "related"
    #        },
    #        {
    #            "candidate_number": 3,
    #            "relation_type": "related"
    #        }
    #     ]
    # }
    
    parsed = json.loads(answer)

    # map candidate numbers back to real note UUIDs and package into LinkSuggestion
    suggestions = []


if __name__ == "__main__":
    # from pprint import pprint

    test_approved_note = """
    SQLite foreign keys are not always enforced by default.
    You may need to enable PRAGMA foreign_keys = ON for each connection.
    """

    test_candidates = [
        NoteOverview(
            id="note-001",
            title="SQLite connection setup",
            updated_at="2026-06-11",
        ),
        NoteOverview(
            id="note-002",
            title="FastAPI request body validation",
            updated_at="2026-06-11",
        ),
        NoteOverview(
            id="note-003",
            title="Database constraints and relationships",
            updated_at="2026-06-11",
        ),
    ]

    result = suggest_links(test_approved_note, test_candidates)

    print(result)