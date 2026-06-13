from pydantic import BaseModel

class FormatNoteRequest(BaseModel):
    """Data model for note formatting request.
    
    Attributes:
        content: string.
    """
    content: str

class NoteContent(BaseModel):
    """uuid and content for a note.
    
    Attributes:
        id: string.
        content: string.
    """
    id: str
    content: str

class NoteOverview(BaseModel):
    """Metadata for note overview and link candidate suggestions.
    
    Attributes:
        id: string.
        title: string.
        updated_at: string.
    """
    id: str
    title: str
    updated_at: str

class LinkSuggestion(BaseModel):
    """Data model for link suggestions returned by LLM.
    
    Attributes:
        candidate_id: string.
        relation_type: string.
    """
    candidate_id: str
    relation_type: str
