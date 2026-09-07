import { useState, useEffect } from 'react'
import { AppShell, Group, Button } from '@mantine/core'
import { notifications } from '@mantine/notifications'

import Home from './components/home/Home.tsx'
import NoteCreationFlow from './components/noteCreation/NoteCreationFlow.tsx'
import NoteView from './components/notePage/NoteView.tsx'
import { postNote } from './api/client.ts'
import type {
  NewNoteInput,
  FormattedNote,
} from './api/types.ts'

import './App.css'


type AppState =
  | {
      screen: 'home'
      recentlyCreatedNodeId: string | null
    }
  | {
      screen: 'noteCreation'
      originalInput: NewNoteInput
      initialFormatted: FormattedNote
    }
  | {
      screen: 'noteView'
      noteId: string
    }


function App() {
  const [appState, setAppState] = useState<AppState>({
    screen: 'home',
    recentlyCreatedNodeId: null
  })
  const [isCreatingNote, setIsCreatingNote] = useState(false)
  const [isNavbarExpanded, setIsNavbarExpanded] = useState(false)

  const recentlyCreatedNodeId = appState.screen === 'home' ? appState.recentlyCreatedNodeId : null

  useEffect(() => {
  if (!recentlyCreatedNodeId) {
    return
  }

    const timeout = setTimeout(() => {
      setAppState((currentState) => {
        if (currentState.screen !== 'home') {
          return currentState
        }

        return {
          ...currentState,
          recentlyCreatedNodeId: null,
        }
      })
  }, 10_000)

  return () => clearTimeout(timeout)
  }, [recentlyCreatedNodeId])

  // Return to Home (Graph view) without new node highlight
  function returnHome() {
    setAppState({
      screen: 'home',
      recentlyCreatedNodeId: null,
    })
  }

  // Return to Home (Graph view) with new node highlight
  function completeNoteCreation(nodeId: string) {
    setAppState({
      screen: 'home',
      recentlyCreatedNodeId: nodeId,
    })
  }

  // Navigate to note view using specific note's id
  function openNote(noteId: string) {
    setAppState({
      screen: 'noteView',
      noteId,
    })
  }

  // Clear highlight for recently created node
  function clearRecentlyCreatedNode() {
    setAppState((currentState) => {
      if (currentState.screen !== 'home') {
        return currentState
      }

      return {
        ...currentState,
        recentlyCreatedNodeId: null,
      }
    })
  }

  async function beginNoteCreation(originalInput: NewNoteInput) {
    setIsCreatingNote(true)

    try {
      const initialFormatted = await postNote(originalInput)

      setAppState({
        screen: 'noteCreation',
        originalInput,
        initialFormatted,
      })
    } catch (error) {
      console.error(error)

      notifications.show({
        title: 'Could not create note',
        message: 'The note could not be formatted. Please try again.',
        color: 'red',
      })
    } finally {
      setIsCreatingNote(false)
    }
  }

  function renderCurrentScreen() {
    switch (appState.screen) {
      case 'home':
        return (
          <Home
            onBeginNoteCreation={beginNoteCreation}
            isCreatingNote={isCreatingNote}
            recentlyCreatedNodeId={appState.recentlyCreatedNodeId}
            onClearRecentNode={clearRecentlyCreatedNode}
            onOpenNote={openNote}
          />
        )

      case 'noteCreation':
        return (
          <NoteCreationFlow
            originalInput={appState.originalInput}
            initialFormatted={appState.initialFormatted}
            onExit={returnHome}
            onComplete={completeNoteCreation}
          />
        )

      case 'noteView':
        return (
          <NoteView
            noteId={appState.noteId}
            onBack={returnHome}
          />
        )
    }
  }

  return (
    <AppShell
      layout="alt"
      header={{ height: 80 }}
      navbar={{
        width: isNavbarExpanded ? 220 : 48,
        breakpoint: 'sm',
      }}
    >
      <AppShell.Navbar p="xs">
        {isNavbarExpanded ? (
          <>
            <Group justify="flex-end">
              <Button
                onClick={() => setIsNavbarExpanded(false)}
                px="xs"
              >
                ‹
              </Button>
            </Group>

            <Button
              onClick={returnHome}
              fullWidth
            >
              Home
            </Button>
          </>
        ) : (
          <Button
            onClick={() => setIsNavbarExpanded(true)}
            px={0}
            fullWidth
          >
            ›
          </Button>
        )}
      </AppShell.Navbar>

      { renderCurrentScreen() }

    </AppShell>
  )
}


export default App