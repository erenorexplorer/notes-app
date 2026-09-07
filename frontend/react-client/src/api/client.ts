import createClient from 'openapi-fetch'
import type { paths } from './generated/schema'
import type { NewNoteInput, FormattedNote, LinkSuggestion, ApprovedLink } from './types'
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

if (!apiBaseUrl) {
  throw new Error('API_BASE_URL is not configured')
}

export const client = createClient<paths>({
  baseUrl: apiBaseUrl,
})

export async function getGraph() {
  const { data, error } = await client.GET('/graph')

  if (error) {
    throw new Error('Failed to load graph')
  }

  return data
}

export async function postNote(newNote: NewNoteInput) {
  const { data, error } = await client.POST('/notes', {
    body: newNote
  })

  if (error) {
    throw new Error('Failed to create formatted note')
  }

  return data
}

export async function approveNote(approvedNote: FormattedNote) {
  const { data, error } = await client.PUT(
    '/notes/{uid}/approve',
    {
      params: {
        path: {
          uid: approvedNote.id,
        },
      },
      body: approvedNote,
    },
  )

  if (error) {
    throw new Error('Failed to approve formatted note')
  }

  return data
}

export async function approveLinks(sourceNoteID: string, selectedLinks: LinkSuggestion[]) {
  const approvedLinkPayload: ApprovedLink[] = selectedLinks.map((link) => ({
    candidate_id: link.candidate_id,
    relation_type: link.relation_type,
  }))

  const { error } = await client.POST(
    '/notes/{uid}/links/approve',
    {
      params: {
        path: {
          uid: sourceNoteID,
        },
      },
      body: approvedLinkPayload,
    },
  )

  if (error) {
    throw new Error('Failed to approve links')
  }
}

// get full note for viewing
export async function getNote(noteId: string) {
  const { data, error } = await client.GET(
    '/notes/{uid}',
    {
      params: {
        path: {
          uid: noteId
        },
      },
    },
  )

  if (error) {
    throw new Error('Failed to load note')
  }

  return data
}