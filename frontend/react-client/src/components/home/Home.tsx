import { useState } from 'react'
import { Button } from '@mantine/core'

import ScreenLayout from '../ScreenLayout'
import GraphView from './GraphView'
import NewNotePanel from './NewNotePanel'

import type { NewNoteInput } from '../../api/types'

type HomeProps = {
  onBeginNoteCreation: (input: NewNoteInput) => void
  isCreatingNote: boolean                 // True = format note request being processed
  recentlyCreatedNodeId: string | null
  onClearRecentNode: () => void           // Clear highlight for newest node
  onOpenNote: (noteId: string) => void    // Call App.tsx function to navigate to note view for specific note by id, called by graphview on node click etc.
}

function Home({ onBeginNoteCreation, isCreatingNote, recentlyCreatedNodeId, onClearRecentNode, onOpenNote }: HomeProps) {
  const [isPanelOpen, setIsPanelOpen] = useState(false)

  function beginNoteCreation(input: NewNoteInput) {
    setIsPanelOpen(false)
    onBeginNoteCreation(input)
  }

  return (
    <ScreenLayout title="Graph View"
      right={
        <Button onClick={() => setIsPanelOpen(true)} loading={isCreatingNote}>
          New note
        </Button>
      }
      panel={
        <NewNotePanel
          opened={isPanelOpen}
          onClose={() => setIsPanelOpen(false)}
          onSubmit={beginNoteCreation}
        />
      }
    >
      <GraphView
        recentlyCreatedNodeId={recentlyCreatedNodeId}
        onClearRecentNode={onClearRecentNode}
        onOpenNote={onOpenNote}
      />
    </ScreenLayout>
  )
}

export default Home