---
title: Theme Tools
slug: theme-tools
order: 40
section: Getting Started
---

`ophix-admin-interface` provides management commands for working with Django admin themes.
Themes can be activated, titled, listed, exported, imported, and deleted — all via
`ophix-manage`.

---

## set\_theme

Activate a theme by name. Only one theme can be active at a time; activating a new theme
automatically deactivates the current one.

```bash
ophix-manage set_theme Midnight
```

Omit the name to pick interactively from the list of installed themes:

```bash
ophix-manage set_theme
```

Theme names are case-sensitive and must match exactly what is stored in the database.

In production (`DEBUG=False`), `set_theme` automatically runs `collectstatic` after
activating the theme and reminds you to restart the service:

```bash
sudo systemctl restart <slug>
```

The restart is required because gunicorn workers cache the static file manifest in memory.
Without it the server may still reference the old static file URLs.

To skip `collectstatic` (for example, in a scripted workflow where you plan to run it
separately):

```bash
ophix-manage set_theme Midnight --no-collectstatic
```

If the activated theme has no title set, set the server title in the **Settings** admin
page (title is managed there, not per-theme — see `ophix-admin-settings`).

### Changing theme via the admin UI

If you activate a theme through the Django admin interface rather than via `set_theme`,
`collectstatic` does not run automatically. If the browser still shows the old theme after
switching, run:

```bash
ophix-manage collectstatic --noinput
sudo systemctl restart <slug>
```

---

## list\_themes

List all themes currently in the database.

```bash
ophix-manage list_themes
```

Show full detail including active status, title, env name, source package, and version:

```bash
ophix-manage list_themes --details
```

The `--details` output cross-references installed themes against the `ophix.plugins` entry
points to identify which pip package each theme came from.

---

## export\_theme

Export a theme to a portable `.tar.gz` archive containing the theme JSON and its media
files (logo, favicon).

```bash
ophix-manage export_theme Midnight
ophix-manage export_theme Midnight --output ./exports/
```

Strip environment-specific metadata before exporting (useful when sharing themes between
servers):

```bash
ophix-manage export_theme Midnight --strip-title --strip-env-name
```

Rename the theme in the export:

```bash
ophix-manage export_theme Midnight --rename MyBranding
```

| Option | Description |
| --- | --- |
| `--output <dir>` | Output directory (defaults to `BASE_DIR`) |
| `--strip-title` | Remove the title from the exported JSON |
| `--strip-env-name` | Remove the env\_name from the exported JSON |
| `--rename <name>` | Rename the theme inside the export |

---

## import\_theme

Import a theme from a `.tar.gz` archive produced by `export_theme`.

```bash
ophix-manage import_theme exports/Midnight_theme.tar.gz
```

Rename or override fields on import:

```bash
ophix-manage import_theme exports/Midnight_theme.tar.gz --rename Staging --title "Staging"
```

Overwrite an existing theme with the same name:

```bash
ophix-manage import_theme exports/Midnight_theme.tar.gz --force
```

| Option | Description |
| --- | --- |
| `--rename <name>` | Rename the theme on import |
| `--title <title>` | Override the theme title |
| `--env-name <env>` | Override the env\_name |
| `--force` | Overwrite an existing theme with the same name |

---

## delete\_theme

Delete a theme by name, including its namespaced media directory.

```bash
ophix-manage delete_theme OldTheme
```

Keep the media files on disk (database record removed, files preserved):

```bash
ophix-manage delete_theme OldTheme --preserve-media
```

Force deletion of the currently active theme (not recommended — activate another theme
first with `set_theme`):

```bash
ophix-manage delete_theme OldTheme --force
```

The system must always have at least one theme. Deleting the last remaining theme is
refused regardless of flags.

| Option | Description |
| --- | --- |
| `--preserve-media` | Remove the database record but leave media files on disk |
| `--force` | Allow deletion of the active theme |

**Note — bundled themes return on next migrate:** The built-in **Ophix** theme is
reinstalled automatically every time `ophix-manage migrate` runs (via the `post_migrate`
signal in `ophix-admin-interface`). If you delete it, it will come back on the next
migration or upgrade. This is by design — the bundled theme is always available as a
fallback. To use a different theme permanently, activate it with `set_theme` and leave
the Ophix theme inactive; there is no need to delete it.

---

## Server settings

| Variable | Default | Description |
| --- | --- | --- |
| `SHOW_THEME_MODEL` | `False` | Show the Themes model in the admin navigation. Only needed if you want to manage themes directly through the database UI rather than via the commands above. |
