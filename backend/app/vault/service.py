from datetime import datetime
import uuid
from app.vault import model
from app.schemas import FullNote, NoteOverview, LinkSuggestion, GraphData, GraphNode, GraphEdge

# future: function to return large DTO of whole vault structure
# i.e. stitch together notes and links.
# using model's getallnotes and getalllinks

def create_raw_note(raw:str) -> str:
    """Create a new note with raw note and return uuid"""
    uid = str(uuid.uuid4())
    create_time = datetime.now()
    model.insert_note(uid, raw, create_time)
    return uid

def save_approved_note(uid:str, title: str, approved_note:str):
    """Update note with approved note and change status to 'approved'"""
    update_time = datetime.now()
    model.update_approved_note(uid, title, approved_note, update_time)

def get_note_overviews() -> list[NoteOverview]:
    """Return list of note overviews for all notes in vault"""
    rows = model.select_note_overviews()
    return [
        NoteOverview(
            id=row["id"],
            title=row["title"],
            updated_at=row["updated_at"],
        )
        for row in rows
    ]

def get_full_note(uid:str) -> FullNote:
    """Return full note data for a given note id"""
    note_data = model.select_note(uid)
    full_note = FullNote(
        id=uid,
        title=note_data["title"],
        raw_note=note_data['raw_note'],
        approved_note=note_data['approved_note'],
        created_at=note_data['created_at'],
        updated_at=note_data['updated_at']
    )
    return full_note

def save_approved_links(uid:str, approved_links:list[LinkSuggestion]):
    """Saved approved links to database"""

    time = datetime.now()
    link_rows = [
        {
            'link_id': str(uuid.uuid4()),
            'source_note': uid,
            'target_note': link.candidate_id,
            'relation_type': link.relation_type,
            'created_at': time,
        }
        for link in approved_links
    ]
    model.insert_approved_links(link_rows)

def get_graph_data() -> GraphData:
    node_data = model.select_note_previews()
    link_data = model.select_all_links()
    valid_nodes = {node['id'] for node in node_data}

    print(node_data)
    graph_data = GraphData(
        nodes = [
            GraphNode(
                id=node['id'],
                title=node['title'],
                preview=node['approved_note']
            )
            for node in node_data
        ],
        links = [
            GraphEdge(
                id=link['id'],
                source_id=link['source_note'],
                target_id=link['target_note'],
                relation_type=link['relation_type']
            )
            for link in link_data 
            if link['source_note'] in valid_nodes and link['target_note'] in valid_nodes
        ]
    )

    return graph_data