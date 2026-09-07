import { useState } from 'react'
import {
  Badge,
  Box,
  Button,
  Checkbox,
  Divider,
  Group,
  ScrollArea,
  Stack,
  Text,
  Title,
} from '@mantine/core'

import classes from './ReviewLinksView.module.css'
import type { LinkSuggestion, FormattedNote } from '../../api/types'

type ReviewLinksViewProps = {
  sourceNote: FormattedNote
  suggestedLinks: LinkSuggestion[]
  onSkip: () => void
  onSave: (sourceNoteID: string, selectedLinks: LinkSuggestion[]) => void
  isLoading: boolean
}

function ReviewLinksView({
  sourceNote,
  suggestedLinks,
  onSkip,
  onSave,
  isLoading
}: ReviewLinksViewProps) {
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  // const [manualSearch, setManualSearch] = useState('')

  function toggleSuggestion(id: string) {
    setSelectedIds((currentIds) =>
      currentIds.includes(id)
        ? currentIds.filter((currentId) => currentId !== id)
        : [...currentIds, id],
    )
  }

  function handleSave() {
    const selectedLinks = suggestedLinks.filter((suggestion) =>
      selectedIds.includes(suggestion.candidate_id),
    )
    onSave(sourceNote.id, selectedLinks)
  }

  return (
    <Box className={classes.root}>
      {/* Left pane: approved note */}
      <Box component="section" className={classes.notePane}>
        <Group justify="space-between" p="md">
          <Text fw={600}>Approved note</Text>
          <Badge variant="light">Read-only</Badge>
        </Group>

        <Box px="md" pb="md">
          <Title order={2}>{sourceNote.title}</Title>
        </Box>

        <Divider />

        <ScrollArea
          className={classes.noteScroll}
          type="auto"
          offsetScrollbars
        >
          <Text className={classes.noteBody}>
            {sourceNote.content}
          </Text>
        </ScrollArea>
      </Box>

      {/* Right pane: suggested links */}
      <Box component="aside" className={classes.linksPane}>
        <Box p="md">
          <Title order={3}>Suggested links</Title>

          <Text c="dimmed" size="sm" mt={4}>
            Select connections that would help you find this note later.
          </Text>
        </Box>

        <ScrollArea
          className={classes.suggestionsScroll}
          type="auto"
          offsetScrollbars
        >
          <Stack gap={0}>
            {suggestedLinks.map((suggestion) => {
              const checked = selectedIds.includes(suggestion.candidate_id)

              return (
                <Checkbox.Card
                  key={suggestion.candidate_id}
                  checked={checked}
                  onClick={() => toggleSuggestion(suggestion.candidate_id)}
                  className={classes.suggestionCard}
                >
                  <Group
                    wrap="nowrap"
                    align="flex-start"
                    gap="md"
                  >
                    <Checkbox.Indicator checked={checked} />

                    <Box className={classes.suggestionContent}>
                      <Group
                        justify="space-between"
                        align="flex-start"
                        wrap="nowrap"
                      >
                        <Text fw={600}>
                          {suggestion.candidate_title}
                        </Text>

                        <Badge
                          variant="outline"
                          size="sm"
                          color="gray"
                        >
                          {suggestion.relation_type}
                        </Badge>
                      </Group>

                      {/* <Text
                        c="dimmed"
                        size="sm"
                        mt="xs"
                      >
                        {suggestion.reasoning}
                      </Text> */}
                    </Box>
                  </Group>
                </Checkbox.Card>
              )
            })}
          </Stack>
        </ScrollArea>

        {/* <Box className={classes.manualLinkSection} p="md">
          <Text fw={600} mb="sm">
            Add a link the AI missed
          </Text>

          <TextInput
            aria-label="Search existing notes"
            placeholder="Search notes..."
            value={manualSearch}
            onChange={(event) =>
              setManualSearch(event.currentTarget.value)
            }
          />
        </Box> */}

        <Divider />

        <Group
          className={classes.actions}
          justify="flex-end"
          p="md"
        >
        <Button
          variant="default"
          onClick={onSkip}
          disabled={isLoading}
        >
          Skip
        </Button>

        <Button onClick={handleSave} loading={isLoading}>
          Save selected links
        </Button>
        </Group>
      </Box>
    </Box>
  )
}

export default ReviewLinksView