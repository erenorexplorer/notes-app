from openai import OpenAI

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
                    "Preserve meaning. Do not invent facts. Keep the result concise and reviewable."
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