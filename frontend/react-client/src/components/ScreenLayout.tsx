import type { ReactNode } from 'react'
import { AppShell, Group, Title } from '@mantine/core'

type ScreenLayoutProps = {
  title: string
  right?: ReactNode         // Buttons on right of header box
  panel?: ReactNode         // New Note Drawer on screen right
  children: ReactNode
}

function ScreenLayout({ title, right, panel, children }: ScreenLayoutProps) {
  return (
    <>
      <AppShell.Header p="xs">
        <Group
          justify="space-between"
          align="center"
          h="100%"
        >
          <Title>{title}</Title>
          {right}
        </Group>
      </AppShell.Header>

      <AppShell.Main>
        {children}
      </AppShell.Main>

      {panel}
    </>
  )
}

export default ScreenLayout