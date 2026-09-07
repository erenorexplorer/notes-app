import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { MantineProvider } from '@mantine/core'
import { splitPaneDark } from './theme/theme.ts'
import { Notifications } from '@mantine/notifications'

import '@mantine/core/styles.css'
import '@mantine/notifications/styles.css'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider theme={splitPaneDark} defaultColorScheme='dark'>
      <Notifications />
      <App />
    </MantineProvider>
  </StrictMode>,
)
