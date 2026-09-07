import { useState } from 'react'
import {
  Button,
  Drawer,
  Group,
  Stack,
  Textarea,
  TextInput,
  Text,
} from '@mantine/core'
import type { NewNoteInput } from '../../api/types'

type NewNotePanelProps = {
  opened: boolean
  onClose: () => void
  onSubmit: (input: NewNoteInput) => void
}

function NewNotePanel({ opened, onClose, onSubmit }: NewNotePanelProps) {
  const [newNoteTitle, setNewNoteTitle] = useState('')
  const [rawNote, setRawNote] = useState('')

  const trimmedTitle = newNoteTitle.trim()
  const trimmedNote = rawNote.trim()
  

  function handleClose() {
    setNewNoteTitle('')
    setRawNote('')
    onClose()
  }

  function handleSubmit() {
    if (!trimmedTitle || !trimmedNote) {
      return
    }

    const input: NewNoteInput = {
      title: trimmedTitle,
      content: trimmedNote,
    }

    onSubmit(input)
  }

  return (
    <Drawer
      opened={opened}
      onClose={handleClose}
      position="right"
      size="md"
      title="Create a new note"
    >
      <form
        onSubmit={(event) => {
          event.preventDefault()
          handleSubmit()
        }}
      >
        <Stack>
          <Text size="sm" c="dimmed">
            Paste or write the rough note you want to process.
          </Text>
          <TextInput
            data-autofocus
            placeholder="Put your title here..."
            value={newNoteTitle}
            onChange={(event) =>
              setNewNoteTitle(event.currentTarget.value)
            }
          >
          </TextInput>
          <Textarea
            placeholder="Put your note here..."
            value={rawNote}
            onChange={(event) =>
              setRawNote(event.currentTarget.value)
            }
            minRows={20}
            maxRows={30}
            autosize
          />

          <Group justify="flex-end">
            <Button
              type="button"
              variant="default"
              onClick={handleClose}
            >
              Cancel
            </Button>

            <Button
              type="submit"
              disabled={!trimmedTitle || !trimmedNote}
            >
              Continue
            </Button>
          </Group>
        </Stack>
      </form>
    </Drawer>
  )
}

export default NewNotePanel