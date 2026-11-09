# Prototypes

Screens sketched from __DESIGN_SYSTEM__, one file each. This folder is maintained by the ui-prototyping plugin for
Claude Code: ask it to make, change, open, list or delete a prototype.

```
__COMMAND__
```

`http://localhost:__PORT__/` lists the prototypes; `http://localhost:__PORT__/<name>` opens one. An open page updates
itself when its file changes.

A prototype is `<name>.tsx` in this folder. It default-exports a component, and its first line is a comment saying
what it shows. It may import only __ALLOW__ and files in this folder; `_*.tsx` files hold shared fake data and are
not prototypes. A prototype is a reference for a feature, not the feature: it makes no API calls.

`vite.config.mjs` serves them. Its `settings` block names the styles every prototype loads, the providers that wrap
it, and what it may import.

## The design system

<!-- What it is, where it lives, how it is imported: one paragraph. -->

Every prototype loads __STYLES__ and is wrapped in __FRAME__, as the app's screens are.

### Components

<!-- One row per component a screen is built from. Props: the ones that change how it looks, with their values. -->

| Component | For | Props |
|---|---|---|

### Tokens

<!-- The names a prototype may use for colour, spacing, radius and type: utility classes or CSS variables. -->

### Patterns

<!-- How the app composes them: page layout, a list, a form, an empty state. Where to see each one. -->
