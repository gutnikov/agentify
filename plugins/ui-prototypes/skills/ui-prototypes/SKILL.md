---
name: ui-prototypes
description: Sketches screens from a project's own design system and serves them at a local URL. Finds the project's design-system components, sets up one command that starts a dev server for prototypes, and makes, changes, opens, lists and deletes named prototypes, each saved as one file so that it can be opened again. Use when the user wants to mock up or prototype a screen, a flow or a layout with the project's components, see an idea in the browser before building it, set up prototyping for a project, or open, list or delete a prototype. Not for building the real feature.
---

# UI prototypes

A **prototype** is one file that composes the project's design-system components into a screen. A dev server shows
it at `http://localhost:<port>/<name>`. It is a reference for a feature, not the feature: it makes no API calls and
never ships.

## What lives in the project

As little as possible. Every file you add is one more the team carries, so add only these:

| Path | What |
|---|---|
| `<host>/prototypes/vite.config.mjs` | the runner: serves the prototypes; from `$S/templates/vite.config.mjs` |
| `<host>/prototypes/README.md` | that this folder is maintained by this plugin, the command, and the design-system catalog |
| `<host>/prototypes/<name>.tsx` | one per prototype |
| `"proto"` in `<host>/package.json` | the script that starts the server: `vite --config prototypes/vite.config.mjs` |

No `index.html`, entry file, `tsconfig`, Storybook or new dependency: the runner makes the page and the entry itself.
`<host>` is the package that depends on the design system, `react`, `react-dom` and `vite`: the app in a monorepo
(`apps/web`), or the root in a single-package project. Prototypes must sit inside it, so that their imports resolve
from its `node_modules`.

## Rules

- **Only the design system.** A prototype imports what `allow` in the runner's settings lists (the design system and
  `react`) and files in its folder. The runner refuses any other import, with the file and line, on the page. That
  is what keeps a prototype from growing into a feature.
- **Components before `className`.** Build from the design system's components and layout primitives; use utility
  classes or tokens for the one-off. A prototype built from the real parts reads as the product.
- **Data that breaks layouts.** Fill lists with long names, large numbers, missing fields and an empty state, not three
  tidy rows. Shared fake data goes in `_<name>.tsx` files in the folder.
- **Use what exists.** If the project already has a way to prototype (a scratchpad route, a Storybook section for
  screens), say so and use it, unless the user asks for this one.
- **Show before you change the project.** The setup's files, the script and any edit to a lint or type-check config
  are shown first and made once the user agrees. Prototypes themselves need no confirmation.

## Talking to the user

- Talk in the user's language.
- Answer with the screen: the URL and a screenshot, not a description.
- Do not ask what you can find out from the code. One question at a time, with the session's question tool, 2–4
  options, the recommended one first.

## Setup: once per project

Run this when the project has no `prototypes/vite.config.mjs`.

1. **Find the design system**, without asking:
   - the components: a workspace package (`packages/ui`, `design-system`), a folder (`src/components/ui`), or a library
     in `package.json` (`@mui/material`, `antd`, `@chakra-ui/react`, `@mantine/core`, Radix with shadcn's
     `components/ui`); its entry point and what it exports;
   - how to use them: `*.stories.*`, docs such as `DESIGN.md`, the props in each component's source, and screens in
     the app that compose them;
   - what a screen needs around it: the styles the app's entry point imports first (`main.tsx`, `index.css`), and the
     providers it wraps the app in (theme, translations, query client). A router provider is needed only if the
     components use router hooks or links;
   - the tokens: CSS variables, a Tailwind `@theme`, a theme object;
   - the host package, and whether it has `vite` and `@vitejs/plugin-react`. Note `@tailwindcss/vite` if the app uses
     Tailwind 4.
2. **Check what fits.** The runner is for React with Vite.
   - If the host has no `vite` or `@vitejs/plugin-react`, they are two dev dependencies to add: propose it.
   - Another framework (Vue, Svelte) needs the runner's entry rewritten for it: say so and propose it before you
     write anything.
3. **Write the runner**: copy `$S/templates/vite.config.mjs` to `<host>/prototypes/` and fill in its placeholders and
   `settings`:
   - `styles`: the app's global stylesheet, as a path relative to the folder, or the design system's stylesheet;
   - `frame`: the providers, as `{ module, export }`. If the app has no single component for them, add one small
     `_frame.tsx` to the folder and point at it;
   - `allow`: the design system's import name and `react`;
   - `port`: a free one near 6060;
   - the plugins: drop `tailwindcss` when the app does not use Tailwind 4, and add any plugin the design system needs
     to compile (the app's `vite.config` shows which).
4. **Write the README** from `$S/templates/README.md`: fill in the placeholders and the catalog of components, props,
   tokens and patterns. The catalog is what you read before every prototype, so make it complete and short.
5. **Add the script** `"proto": "vite --config prototypes/vite.config.mjs"` to the host's `package.json`. The one
   command for the user is `pnpm --filter <host> proto` (or `npm run proto -w <host>`) in a monorepo, and
   `npm run proto` otherwise.
6. **Keep the project's checks green.** If the project's lint or type check covers the folder (`biome check .`, an
   `include` of `**/*`), propose excluding it with one line in that config; prototypes are never type-checked or
   linted.
7. **Prove it**: start the server, write a prototype named `example` that uses the most common components, and check
   it (below). Report the command, the URL and a screenshot.

## Making a prototype

1. **Name it**: lowercase letters, digits and hyphens. The name is the file name and the URL.
2. **Read the catalog** in the folder's README, and the source or stories of each component you use, for its props.
3. **Write `<name>.tsx`**:

   ```tsx
   // Invoices waiting for approval, with the oldest first.
   import { Button, Card, Stack, Text } from '@acme/ui';

   export default function InvoiceApprovals() {
     return (
       <Stack gap="lg" className="mx-auto max-w-3xl px-4 py-10">
         <Text variant="display">Invoices</Text>
         <Card title="Waiting on you" actions={<Button size="sm">Approve all</Button>}>
           <Text tone="muted">Three invoices, the oldest from Tuesday.</Text>
         </Card>
       </Stack>
     );
   }
   ```

4. **Make sure the server runs**: `curl -s -o /dev/null -w '%{http_code}' http://localhost:<port>/`. If nothing
   answers, start the script in the background and read the URL it prints.
5. **Check it in a browser**: open `http://localhost:<port>/<name>` with the browser tool the session has (Chrome
   DevTools, Playwright, agent-browser). An import the runner refuses or a compile error shows as Vite's overlay; a
   render error shows on the page with its stack; read the console too. Fix it until the page renders clean. Without
   a browser tool, `curl -s http://localhost:<port>/<name>.tsx` returns the compiled module or the error.
6. **Show it**: the URL and a screenshot.

To change a prototype, edit its file. An open page updates itself.

## Open, list, delete

- **Saved.** A prototype is saved once its file exists. It opens again at the same URL whenever the server runs. To
  share it with the team, offer to commit it.
- **Open**: make sure the server runs, then give `http://localhost:<port>/<name>`.
- **List**: the `.tsx` files in the folder, except `_*.tsx`, each with its URL and its first-line comment. The
  server's own list is at `http://localhost:<port>/`.
- **Delete**: name the file and ask, then delete it.

## When the design system changes

New components, renamed props or tokens: update the README's catalog. If the styles or the providers the app loads
changed, update `settings` in the runner. Then open each prototype to see which ones broke, and say which.

## Files

`S` is this skill's folder (Claude Code shows it when the skill loads: "Base directory for this skill").

| Path | What |
|---|---|
| `$S/templates/vite.config.mjs` | The runner: settings, then the code that serves the prototypes |
| `$S/templates/README.md` | The folder's README, with the catalog to fill in |
