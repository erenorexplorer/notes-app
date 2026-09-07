import type { components } from './generated/schema'

export type NewNoteInput =
  components['schemas']['FormatNoteRequest']

export type FormattedNote =
  components['schemas']['NoteContent']

export type LinkSuggestion =
  components['schemas']['LinkSuggestionForReview']

export type GraphData =
  components['schemas']['GraphData']

export type ApprovedLink =
  components['schemas']['LinkSuggestion']

export type NoteDetails =
  components['schemas']['FullNote']