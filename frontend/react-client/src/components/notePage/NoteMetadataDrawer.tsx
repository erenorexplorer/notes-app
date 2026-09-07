import {
  Drawer,
  Stack,
  Text,
  Divider,
} from '@mantine/core'

import type { NoteDetails } from '../../api/types'


type NoteMetadataDrawerProps = {
  opened: boolean
  onClose: () => void
  note: NoteDetails
}


function NoteMetadataDrawer({
  opened,
  onClose,
  note,
}: NoteMetadataDrawerProps) {
  return (
    <Drawer
      opened={opened}
      onClose={onClose}
      position="right"
      title="Note metadata"

      // disable default modal behavior like darken outside and close on clicking elsewhere
      withOverlay={false}
      closeOnClickOutside={false}
      trapFocus={false}
      lockScroll={false}
    >
      <Stack>
        <div>
          <Text fw={600}>
            Created
          </Text>

          <Text c="dimmed">
            {note.created_at}
          </Text>
        </div>

        <div>
          <Text fw={600}>
            Updated
          </Text>

          <Text c="dimmed">
            {note.updated_at}
          </Text>
        </div>

        <Divider />

        <div>
          <Text fw={600} mb="xs">
            Original note
          </Text>

          <Text
            c="dimmed"
            style={{ whiteSpace: 'pre-wrap' }}
          >
            {note.raw_note}
          </Text>
        </div>
      </Stack>
    </Drawer>
  )
}


export default NoteMetadataDrawer