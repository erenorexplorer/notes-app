import { useState } from 'react'
import {
  Badge,
  Box,
  Button,
  Divider,
  Group,
  Stack,
  Text,
  Textarea,
  TextInput,
} from '@mantine/core'
import type { NewNoteInput, FormattedNote } from '../../api/types'

import classes from './ReviewNoteView.module.css'

type ReviewNoteViewProps = {
  originalInput: NewNoteInput
  initialFormatted: FormattedNote
  onApprove: (approvedFormatted: FormattedNote) => void
  onCancel: () => void
  isLoading: boolean
}

function ReviewNoteView({ originalInput, initialFormatted, onApprove, onCancel, isLoading }: ReviewNoteViewProps) {
  const [noteTitle, setNoteTitle] = useState(initialFormatted.title)
  const [noteBody, setNoteBody] = useState(initialFormatted.content)

  function handleApprove() {
    const approvedFormatted: FormattedNote = {
      id: initialFormatted.id,
      title: noteTitle,
      content: noteBody,
    }

    onApprove(approvedFormatted)
  }

  return (
    <Stack
      className={classes.root}
      gap={0}
    >
      <Box
        className={classes.editorPane}
        p="md"
      >
        <Stack
          className={classes.editorContent}
          gap="sm"
        >
          <Group justify="space-between">
            <Text fw={600}>Formatted note</Text>
            <Badge variant="light">Editable draft</Badge>
          </Group>

          <TextInput
            aria-label="Note title"
            value={noteTitle}
            onChange={(event) =>
              setNoteTitle(event.currentTarget.value)
            }
            size="lg"
          />

          <Textarea
            aria-label="Formatted note body"
            value={noteBody}
            onChange={(event) =>
              setNoteBody(event.currentTarget.value)
            }
            className={classes.bodyEditor}
            classNames={{
              wrapper: classes.bodyWrapper,
              input: classes.bodyInput,
            }}
          />
        </Stack>
      </Box>

      <Box px="md" py="sm">
        <Text fw={600} size="sm">
          Original note
        </Text>

        <Text c="dimmed" size="sm" truncate>
          {originalInput.content}
        </Text>
      </Box>

      <Divider />

      <Group justify="flex-end" p="md">
        <Button 
          variant="default"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>

        <Button onClick={handleApprove} loading={isLoading}>
          Approve note
        </Button>
      </Group>
    </Stack>
  )
}

export default ReviewNoteView