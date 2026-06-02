# Ophix Admin Interface Release Notes

## 2026.06.02.01

- Added per-colour dark mode overrides. Each colour field in the theme editor now has a companion "dark?" checkbox and dark colour picker. When checked and a colour is set, that colour is applied under `[data-theme="dark"]`; if the checkbox is unchecked or the colour is blank, the light value is used as fallback. The `[data-theme="dark"]` CSS block is emitted in `base_site.html` alongside the existing `:root` block — only overrides with both checkbox and colour set are emitted.
- Logo preview in the theme editor now shows the logo rendered against the current header background colour at the configured max-height and max-width — updating live as those fields are changed, before saving. Selecting a new logo file also previews it immediately.
- Logo and favicon images now appear above (not beside) the file input controls.

## 2026.06.01.01

- Theme editor section renames: "Generic Links" → **Body Text**, "Save Buttons" → **Buttons**,
  "Delete Buttons" → **Alert Buttons**, "Extended Colors" → **Notification Colors**.
- New theme fields: body font family, body font size, button font size, button border radius,
  module/panel border radius, alert/danger color.
- `css_module_rounded_corners` (boolean) replaced by `css_module_border_radius` (CharField,
  default `4px`). Existing themes retain 4px rounded corners. Theme packages with the old
  boolean key in `theme.json` are unaffected — the key is silently ignored.
- Related Modal fieldset: description added explaining the background overlay concept.
- Logo and favicon fields now show a thumbnail preview of the current image in the editor.
- Color picker: clicking the text input now positions the cursor for direct hex editing only.
  The colour swatch button (to the left of the input) opens the picker as before.

## 2026.05.31.01

- Moved server identity settings (title, title_visible, env_name, env_visible_in_header,
  env_visible_in_favicon) and language chooser settings to the new `ophix-admin-settings`
  package. These are now configured in the **Settings** admin section and apply
  server-wide, independent of the active theme.
- `ophix-admin-settings` is now a required dependency — install it alongside this package.
- Removed `dark_mode_link_lightness` field (full per-colour dark mode coming in a
  future release).
- Removed `custom_css_vars` field.
- Retired `set_title` management command — title is now managed directly in the
  Server Settings admin page.
- `env_color` (environment badge colour) remains in the theme editor under the
  Header section.

## 2026.05.30.09

- Themes list view: `env_name` column now shows with header "Env Name" rather than the
  field's default verbose name ("Name"), which was ambiguous alongside the theme name column.

## 2026.05.30.08

- Added `title` and `env_name` columns to the Themes list view.

## 2026.05.30.07

- Added missing migration `0040`: `dark_mode_link_lightness` verbose name was renamed
  from `"link lightness"` to `"accent lightness"` in 2026.05.30.02 but no migration was
  created, causing `migrate` to report pending model changes.

## 2026.05.30.06

- Documented that the built-in Ophix theme is reinstalled automatically on every
  `migrate` run — operators who delete it should expect it to return. Note added to
  the `delete_theme` section of the Theme Tools docs page.

## 2026.05.30.05

- Fixed language chooser dropdown in dark mode: the OS-rendered options popup showed
  near-invisible text (light header colours on white popup background). Added
  `color-scheme: dark` on the `select` and explicit `background-color`/`color` on
  `option` elements so the popup renders with dark background and readable text.

## 2026.05.30.04

- Standardised theme package media layout to `media/<field>/<filename>` (flat) across all
  Ophix theme packages. External theme packages previously used a redundant deep layout
  (`media/admin-interface/themes/<name>/<field>/<filename>`) that mirrored the MEDIA_ROOT
  destination — unnecessary since `install_bundled_theme` constructs the destination path
  itself. All external packages (ocean, midnight, forest, desert, fastrack, imago, seasons)
  updated to the flat layout in the same release cycle. `install_bundled_theme` code
  simplified accordingly.

## 2026.05.30.03

- Fixed `install_bundled_theme`: the built-in Ophix theme favicon was always copied to
  `logo/` instead of `favicon/` because the code used `parts[3]`, which only worked for
  the (now-retired) deep layout used by external theme packages.

## 2026.05.30.02

- Dark mode accent lightness now applies to docs index section headings and toggle
  buttons as well as generic links; field label renamed from "link lightness" to
  "accent lightness".

## 2026.05.30.01

- Added per-theme `dark_mode_link_lightness` setting: controls how much white is
  mixed into link and heading colours in dark mode. Default 30%. Increase for themes
  with darker accent colours.
- Removed bulk action checkboxes from Themes list view (`actions = None`).

## 2026.05.28.02

- Added inline docs page (Theme Tools) in the Getting Started section, covering all theme
  management commands: `set_theme`, `set_title`, `list_themes`, `export_theme`,
  `import_theme`, `delete_theme`. Loaded automatically by `run_install`; load manually
  with `ophix-manage update_docs --include-app-docs admin_interface`.
- Added `--admin-interface-success-color` to themes

## 2026.05.27.08

- `set_title` now accepts an optional positional argument — `ophix-manage set_title "My Title"`
  sets the title directly without prompting.

## 2026.05.27.0

- `set_theme` now shows a numbered interactive picker when called without a theme name,
  with `[active]` marking the current theme. Ctrl+C cancels cleanly.
- `set_theme` falls back to the interactive picker when the supplied name is not found,
  printing the error before showing the list.

## 2026.05.27.06

- `set_title` prompt now reads `Enter new title [current]:` and Ctrl+C exits cleanly
  with "Cancelled. No changes made." rather than a traceback.

## 2026.05.27.05

- Added `set_title` management command — prompts for a new title on the active theme.
  Enter keeps the existing value; `--clear` removes it; `--use-existing` copies the title
  from a previously active (now inactive) theme.
- `set_theme` and `set_title` now print the correct `systemctl restart` command using
  `SERVICE_NAME` from settings rather than a generic `<slug>` placeholder.
- `set_theme` hints to run `set_title` if the newly activated theme has no title set.
- Removed "Django administration" fallback from `base_site.html` — blank title now renders
  blank in both the browser tab and the branding header.

## 2026.05.27.01

- Fixed `install_bundled_theme` media path detection — field name (`logo`/`favicon`) is now
  read from the correct position in the namespaced layout used by all theme packages
  (`media/admin-interface/themes/<name>/<field>/<file>`). Previously files landed under
  `…/admin-interface/` instead of `…/logo/` or `…/favicon/`.
- `Theme.title` default changed from `"Django administration"` to `""` so new installs
  start with no title unless the operator sets one.

## 2026.05.26.01

- Removed remaining `logo_dark` source references (export_theme, import_theme, utils)
  that were left over after migration 0036 dropped the field
- Added classifiers, keywords, and project URLs to `pyproject.toml` for PyPI publishing
- Added `README.md`

## 2026.05.25.01

- Remove `logo_dark` field — the header background colour is fixed per theme, so a dark-mode logo variant is never needed

## 2026.05.24.01

- Add bundled Ophix theme (logo, favicon) installed automatically on migrate
- Update logo and favicon to match new Ophix branding

## 2026.05.22.01

- Theme deletion now removes the namespaced media directory (`MEDIA_ROOT/admin-interface/themes/<name>/`)
  via `post_delete` signal, covering both UI deletion and the `delete_theme` management command.
  Previously, UI-initiated deletions left media files on disk. `delete_theme --preserve-media` still
  suppresses cleanup when needed.

## 2026.05.21.01

- Fixed migration 0035: `logo_dark` `upload_to` was stored as a static string
  instead of the callable, causing Django to report pending model changes after
  the migration had already been applied.

## 2026.05.20.02

- Fixed bundled Ophix theme media path: logo file was copied to the wrong
  destination under `MEDIA_ROOT`. Restructured bundled `media/` directory to
  use the flat `media/<field>/` layout that `install_bundled_theme` expects.
- `install_bundled_theme` now always copies media files on every migrate run,
  not only when the theme is first installed. Fixes missing assets on existing
  installs after an upgrade.
- Bundled Ophix theme title is now populated from `SERVER_NAME` on first
  install (e.g. "Ophix credserver"). Only fills a blank title — never
  overwrites a value the operator has already set.

## 2026.05.20.01

- Bundled "Ophix" default theme with Ophix Project branding; installed automatically
  on `migrate` — active by default on fresh installs, inactive alongside existing themes.
- Added `logo_dark` field to `Theme` model — optional logo shown when the OS/browser
  is in dark mode. When set, the header logo switches automatically via `<picture>` +
  `prefers-color-scheme: dark`. Leave blank to use the standard logo in all modes.
  Theme authors: store the dark variant in `media/admin-interface/themes/<Name>/logo_dark/`.

## 2026.05.19.01

- Added `OPHIX_RELEASE_NOTES.md` for release notes delivery.
