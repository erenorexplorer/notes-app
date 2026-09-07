from pydantic import BaseModel

class FormatNoteRequest(BaseModel):
    """Data model for note formatting request.
    
    Attributes:
        content: string.
    """
    title: str
    content: str

class NoteContent(BaseModel):
    """uuid and content for a note.
    
    Attributes:
        id: string.
        title: string.
        content: string.
    """
    id: str
    title: str
    content: str

class FullNote(BaseModel):
    """Full note data.
    
    Attributes:
        id: string.
        title: string.
        raw_note: string.
        approved_note: string.
        created_at: string.
        updated_at: string.
    """
    id: str
    title: str
    raw_note: str
    approved_note: str
    created_at: str
    updated_at: str

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

class LinkSuggestionForReview(BaseModel):
    """Link suggestion enriched with candidate data for user review.

    Attributes:
        candidate_id: ID of the suggested candidate note.
        candidate_title: Title of the suggested candidate note.
        relation_type: Type of relationship being suggested.
    """
    candidate_id: str
    candidate_title: str
    relation_type: str

class GraphNode(BaseModel):
    id: str
    title: str
    preview: str

class GraphEdge(BaseModel):
    id: str
    source_id: str
    target_id: str
    relation_type: str

class GraphData(BaseModel):
    nodes: list[GraphNode]
    links: list[GraphEdge]