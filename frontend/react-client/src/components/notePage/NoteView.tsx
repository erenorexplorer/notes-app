import { useEffect, useState } from 'react'
import {
  Box,
  Button,
  Group,
  Loader,
  Stack,
  Text,
  Title,
} from '@mantine/core'
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

import classes from './NoteView.module.css'

import ScreenLayout from '../ScreenLayout'
import NoteMetadataDrawer from './NoteMetadataDrawer'

import { getNote } from '../../api/client'
import type { NoteDetails } from '../../api/types'


type NoteViewProps = {
  noteId: string
  onBack: () => void
}

function NoteView({ noteId, onBack }: NoteViewProps) {
  const [note, setNote] = useState<NoteDetails | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [loadFailed, setLoadFailed] = useState(false)

  const [isMetadataOpen, setIsMetadataOpen] = useState(false)

  useEffect(() => {
    async function loadNote() {
      setIsLoading(true)
      setLoadFailed(false)

      try {
        const loadedNote = await getNote(noteId)
        setNote(loadedNote)
      } catch (error) {
        console.error(error)
        setLoadFailed(true)
      } finally {
        setIsLoading(false)
      }
    }

    loadNote()
  }, [noteId])

    if (isLoading) {
    return (
      <ScreenLayout title="View Note">
        <Group justify="center" p="xl">
          <Loader />
        </Group>
      </ScreenLayout>
    )
  }

  if (loadFailed || !note) {
    return (
      <ScreenLayout
        title="View Note"
        right={
          <Button onClick={onBack}>
            Back to Graph
          </Button>
        }
      >
        <Text p="xl">
          Could not load note.
        </Text>
      </ScreenLayout>
    )
  }

    return (
    <ScreenLayout
      title="View Note"
      right={
        <Group>
          <Button
            variant="default"
            onClick={() => setIsMetadataOpen(true)}
          >
            Details
          </Button>

          <Button onClick={onBack}>
            Back to Graph
          </Button>
        </Group>
      }
      panel={
        <NoteMetadataDrawer
          opened={isMetadataOpen}
          onClose={() => setIsMetadataOpen(false)}
          note={note}
        />
      }
    >
      <Box
        maw={1000}
        mx="auto"
        px="xl"
        py="xl"
      >
        <Stack>
          <Title order={1}>
            {note.title}
          </Title>

          <div className={classes.markdown}>
            <Markdown remarkPlugins={[remarkGfm]}>
              {note.approved_note}
            </Markdown>
          </div>
        </Stack>
      </Box>
    </ScreenLayout>
  )
}


export default NoteView