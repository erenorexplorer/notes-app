import os
from app.llm import service
from app.llm import service_stub
from dotenv import load_dotenv

load_dotenv()

def get_llm_service():
    llm_mode = os.getenv("LLM_MODE", "real")

    if llm_mode == "stub":
        return service_stub
    
    return service