// src/theme.ts
import { createTheme, AppShell, Button, TextInput, Textarea, Title, Text } from '@mantine/core';

// 1. Import your new CSS modules
import buttonClasses from './Button.module.css';
import textInputClasses from './TextInput.module.css';
import textareaClasses from './Textarea.module.css'

export const splitPaneDark = createTheme({
  // Z-Axis Palette
  colors: {
    dark: [
      '#C1C2C5', // dark.0: Primary text
      '#A6A7AB', // dark.1: Muted text
      '#909296', // dark.2: Disabled elements
      '#5C5F66', // dark.3: Floating elements (Z=3: command palettes, popups)
      '#373A40', // dark.4: Hover states (Z=2: active tabs, hovered file names)
      '#2C2E33', // dark.5: Thick borders/dividers
      '#25262B', // dark.6: Subtle structural borders
      '#1E1E1E', // dark.7: Structural Scaffolding (Z=1: Navbar, Aside, Header)
      '#181818', // dark.8: Deep secondary elements
      '#0A0A0A', // dark.9: The Base Canvas (Z=0: Main code editor panel)
    ],
  },

  components: {
    AppShell: AppShell.extend({
        defaultProps: {
            padding: 0,
            withBorder: true, 
        },
        styles: {
            main: { backgroundColor: 'var(--mantine-color-dark-8)' },
            navbar: { backgroundColor: 'var(--mantine-color-dark-7)' },
            header: { backgroundColor: 'var(--mantine-color-dark-7)' },
            aside: { backgroundColor: 'var(--mantine-color-dark-7)' },
        }
    }),

    Button: Button.extend({
        defaultProps: {
            radius: 'xs', 
            variant: 'transparent',
        },
        vars: () => ({
            root: {
                '--button-bg': 'var(--mantine-color-dark-7)',
                '--button-hover': 'var(--mantine-color-dark-6)', 
                '--button-color': 'var(--mantine-color-dark-0)', 
            },
        }),
        // 2. Connect the Button CSS module here
        classNames: buttonClasses, 
    }),

    TextInput: TextInput.extend({
        // 3. Connect the TextInput CSS module here
        classNames: textInputClasses,
    }),

    Text: Text.extend({
        defaultProps: {
            c: 'var(--mantine-color-dark-3)', 
            size: 'sm', 
        }
    }),

    Textarea: Textarea.extend({
        classNames: textareaClasses,
    }),

    Title: Title.extend({
        defaultProps: {
            c: 'var(--mantine-color-dark-1)', 
        },
    }),
  },
});