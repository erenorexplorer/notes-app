import { useState } from 'react'

import ScreenLayout from '../ScreenLayout'
import ReviewNoteView from './ReviewNoteView'
import ReviewLinksView from './ReviewLinksView'
import { notifications } from '@mantine/notifications'

import { approveNote, approveLinks } from '../../api/client'
import type { NewNoteInput, FormattedNote, LinkSuggestion } from '../../api/types'


type NoteCreationFlowProps = {
  originalInput: NewNoteInput
  initialFormatted: FormattedNote
  onExit: () => void                      // Exit creation flow without a new note to identify
  onComplete: (nodeId: string) => void    // Exit creation flow and identify the newly created note for highlight
}

type NoteCreationState =
  | { step: 'reviewNote' }
  | {
      step: 'reviewLinks' 
      approvedFormatted: FormattedNote
      suggestedLinks: LinkSuggestion[]
    }


function NoteCreationFlow({ originalInput, initialFormatted, onExit, onComplete }: NoteCreationFlowProps) {
  const [flowState, setFlowState] = useState<NoteCreationState>({
    step: 'reviewNote',
  })
  const [approveNoteLoading, setApproveNoteLoading] = useState(false)
  const [approveLinksLoading, setApproveLinksLoading] = useState(false)

  async function handleApproveNote(approvedFormatted: FormattedNote) {
    setApproveNoteLoading(true)

    try {
      const suggestedLinks = await approveNote(approvedFormatted)

      setFlowState({
        step: 'reviewLinks',
        approvedFormatted,
        suggestedLinks,
      })
    } catch (error) {
      console.error(error)

      notifications.show({
        title: 'Could not approve note',
        message: 'Link suggestions could not be generated. Please try again.',
        color: 'red',
      })
    } finally {
      setApproveNoteLoading(false)
    }
  }

  async function handleApproveLinks(
    sourceNoteID: string,
    approvedLinks: LinkSuggestion[],
  ) {
    setApproveLinksLoading(true)

    try {
      await approveLinks(sourceNoteID, approvedLinks)

      notifications.show({
        title: 'Note saved',
        message: 'The note and selected links were saved successfully.',
      })

      onComplete(sourceNoteID)
    } catch (error) {
      console.error(error)

      notifications.show({
        title: 'Could not save links',
        message: 'The selected links could not be saved. Please try again.',
        color: 'red',
      })
    } finally {
      setApproveLinksLoading(false)
    }
  }

  switch (flowState.step) {
    case 'reviewNote':
      return (
        <ScreenLayout title="Review Note">
          <ReviewNoteView
            originalInput={originalInput}
            initialFormatted={initialFormatted}
            onApprove={handleApproveNote}
            onCancel={onExit}
            isLoading={approveNoteLoading}

          />
        </ScreenLayout>
      )

    case 'reviewLinks':
      return (
        <ScreenLayout title="Review Links">
          <ReviewLinksView
            sourceNote={flowState.approvedFormatted}
            suggestedLinks={flowState.suggestedLinks}
            onSkip={() =>
              onComplete(flowState.approvedFormatted.id)
            }
            onSave={handleApproveLinks}
            isLoading={approveLinksLoading}
          />
        </ScreenLayout>
      )
  }
}


export default NoteCreationFlow