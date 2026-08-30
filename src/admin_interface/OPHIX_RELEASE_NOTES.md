# Ophix Admin Interface Release Notes

## Unreleased

- Finished the `#user-tools` (top-right "WELCOME,ADMIN. CHANGE PASSWORD / LOG OUT")
  font-weight/alignment fix from the marketing manager's review list — the earlier
  pass only set `font-weight: 400` on the `a` elements, leaving the plain
  "WELCOME,ADMIN." text node and the `#logout-form button` off the same rule; moved
  it onto the `#user-tools` container itself in `header.css` so every child inherits
  consistently. Also added `line-height: 1` to `#logout-form button` (was unset,
  relying on the browser's default button line-height, which is not guaranteed to
  match the surrounding text's line-height across browsers/zoom levels — this is
  what caused "LOG OUT" to look vertically offset from "CHANGE PASSWORD" in one
  browser but not another).

## 2026.08.29.04

- Fixed wide fields (Description/Command textareas, URL fields, etc.) rendering
  full-width on their own row instead of staying beside the label — a side effect of
  `2026.08.29.03`'s `flex-wrap: wrap` addition (needed so `.help`/`.errorlist` fall
  onto their own line). Django's own `.vLargeTextField`/`.vXMLLargeTextField` is a
  fixed 48em, `.vURLField` 30em — wider than the space left after the 160px label
  column. Flexbox gives form controls an "automatic minimum size" floor based on
  their intrinsic/specified size rather than zero, unless overridden; with wrapping
  now enabled, a field whose floor still exceeds the remaining row space wraps onto
  its own line instead of shrinking below it, landing at the container's own left
  edge rather than indented past the label. Fixed with `min-width: 0` on the field
  (deliberately not touching `flex-grow`, which stays at its default `0` — ordinary
  fields keep their natural/specified width, e.g. `.vTextField`'s 20em, rather than
  stretching to fill leftover row space, which would be a new visual change, not a
  restoration of the old behaviour). `.related-widget-wrapper` (FK fields) already
  had this protection; ordinary fields never did.
- All labels and legends now render at a uniform `font-weight: 700`, deliberately
  overriding Django's own required-vs-optional bold/normal distinction
  (`label { font-weight: normal }` / `label.required { font-weight: bold }` — this
  mechanism is unchanged between Django versions, confirmed identical in both CSS and
  `AdminField.label_tag()`; it was never a bug, just no longer a distinction this
  project wants surfaced this way). A blank required field already gets its own clear
  "This field is required." error on submit, so the extra visual hint wasn't valued
  and the inconsistent weight across a form read as untidy instead.
- Fixed every ordinary field sitting 10px further right than intended, discovered via
  the `ScheduledTask` date/time widget looking "slightly off" relative to everything
  around it — the datetime widget hadn't moved, everything else had. Root cause:
  Django 6.1's own `.flex-container` rule added `gap: 10px` (6.0.7 had none at all),
  which none of this session's earlier fixes reset. The label already provides 10px
  of separation via its own `padding: 4px 10px 0 0` — `gap`'s column-gap component
  added a second, independent 10px on top of that, double-counting the spacing for
  every ordinary field. `.datetime-sublabel`'s hand-built CSS doesn't route through
  this same generic container, so it wasn't affected and looked out of step by
  comparison. Fixed with `column-gap: 0` (not the `gap` shorthand) on the base
  `.flex-container` rule — `row-gap` must stay at Django's 10px, since `.help`/
  `div.help` (Django's own `base.css`) carries no margin of its own at all; the
  vertical space between a field's row and its wrapped help-text row underneath
  comes entirely from `row-gap`, and zeroing it too would collapse that spacing
  instead of just the horizontal double-count.

## 2026.08.29.03

- Fixed the remaining pieces of the same Django 6.1 `fieldset.html` restructure from
  `2026.08.29.02`. Django 6.1's per-field DOM order inside `.flex-container` is
  `label -> help -> errors -> field` — both `<div class="help">` and
  `<ul class="errorlist">` (field/line validation errors) now render *before* the
  field itself, whereas in 6.0.7 both were siblings positioned *after* the closing
  `.flex-container` div entirely. Two problems followed from pinning
  `.flex-container` to `flex-direction: row` to fix label/field placement:
  - Help text and errors became ordinary items in that same row instead of falling
    below it (help sat between the label and the field on one line).
  - Naively forcing just `.help` onto its own full-width row via `flex-wrap` +
    `flex: 0 0 100%` doesn't work on its own: flex-wrap doesn't backfill earlier
    rows once one has wrapped, so anything *after* help in DOM order — the
    errorlist, and critically the field itself — would also get pushed onto their
    own separate rows, undoing the label/field pairing for any field with help text
    or a validation error (i.e. most fields).
  - Fixed with `order: 999` on both `.flex-container > .help` and
    `.flex-container > ul.errorlist`, alongside `flex: 0 0 100%`: label and the
    field (whatever it renders as — input/select/textarea/`.related-widget-wrapper`/
    `.readonly`, all left at the default order) settle onto row one together
    regardless of what sits between them in the DOM, while help and errors each
    wrap onto their own full-width row afterward.

## 2026.08.29.02

- Fixed a second Django 6.1 layout regression from the same root cause as
  `2026.08.29.01`'s `.flex-container` fix, missed there because it's a different half
  of the same upstream redesign: **every ordinary field's label and input rendered
  stacked in a single column instead of side by side.** Checked Django's actual
  `fieldset.html` include template directly (not just CSS) — every field, not just
  checkboxes, is wrapped in `<div class="flex-container fieldBox ...">{{ label }}{{
  field }}</div>` in both 6.0.7 and 6.1. The `2026.08.29.01` fix only pinned
  `flex-direction: row` on `.flex-container.checkbox-row`, missing that the *base*
  `.flex-container` rule needed it too, since ordinary fields use only the base class.
  Django 6.1 also deleted `.aligned legend, .aligned label { display: block; width:
  160px; ... }` from its own forms.css entirely with no replacement — the other half of
  the same redesign (their new column-based layout no longer needs a fixed label
  width). Fixed by moving `flex-direction: row` onto the base `.flex-container` rule
  (removing it from `.checkbox-row`, now redundant) and restoring the `.aligned label`
  rule verbatim from Django's own pre-6.1 CSS. The 160px value isn't arbitrary — it's
  already depended on directly by `.aligned p.datetime .datetime-sublabel`'s own
  comment ("matches Django's .aligned label column").

## 2026.08.29.01

- Fixed several layout regressions under Django 6.1, all caused by the same root pattern:
  our CSS relied on Django's own base admin CSS to supply a `display`/direction/spacing
  declaration we never set explicitly ourselves, and Django 6.1 changed several of those
  defaults.
  - **Boolean field checkboxes rendered stacked/centered instead of in a row.** Django
    6.1's `.flex-container` base rule gained `flex-direction: column` (previously
    undeclared, defaulting to the browser's `row`). Our `.flex-container.checkbox-row`
    override never declared its own direction, so it silently inherited whichever default
    Django supplied. Fixed by declaring `display: flex` on the `.flex-container` base rule
    and `flex-direction: row` on `.checkbox-row` explicitly.
  - **Breadcrumbs lost their theme color on every standard admin page, and lost their
    padding on custom pages with a hardcoded breadcrumb (e.g. the Client Management Status
    page).** Django 6.1 changed its own breadcrumb markup from `<div class="breadcrumbs">`
    to a semantic `<ol class="breadcrumbs"><li>...</li></ol>` (accessibility improvement)
    and dropped its `div.breadcrumbs` CSS rule entirely in favor of `ol.breadcrumbs`. Our
    own `.admin-interface div.breadcrumbs` selector was tag-locked, so it stopped matching
    Django's own breadcrumb block (theme color silently lost, falling back to Django's
    generic un-themed blue) while a custom template hardcoding its own `<div
    class="breadcrumbs">` kept matching our rule but lost all padding (nothing supplied it
    anymore, since Django removed its own `div.breadcrumbs` rule). Fixed by broadening the
    selector to `.admin-interface .breadcrumbs` (class-only, matches both forms) and
    declaring `padding`/`margin`/`border` explicitly instead of relying on Django's base
    CSS for them.
  - Also hardened two spots that hadn't broken yet but shared the identical risk: `.submit-row`
    (Save/Continue/Delete button ordering) and `#main` (the nav-sidebar/content flex split)
    now both declare `display: flex` explicitly instead of depending on Django's own base
    CSS to supply it.

## 2026.08.12.01

- Django dependency split by `python_version` marker: `Django>=4.2,<6.0` on Python < 3.12,
  `Django>=4.2` (no upper bound) on Python >= 3.12. Django 6.0 itself requires Python 3.12+;
  this makes the "Python 3.10/3.11 + Django 6" combination structurally unreachable via pip's
  resolver instead of failing at runtime, while still allowing 3.10/3.11 hosts to run on
  Django 5.2. `requires-python` is unchanged (`>=3.10` remains the true floor).

## 2026.08.04.01

- `export_theme` gains a `--stable` flag, written for `ophix-revisions`. This command
  doesn't follow the `_build_meta`/payload-envelope pattern used elsewhere — it's a
  `dumpdata`-based `.tar.gz` bundle, so `--stable` fixes two independent embedded-timestamp
  sources instead: `sort_keys=True` on the fixture JSON, and zeroed mtime/ownership on every
  tar entry plus a zeroed gzip header timestamp (Python's `tarfile.open(path, "w:gz")`
  shortcut has no way to override either of the latter two — fixed by building the archive
  via an explicit `gzip.GzipFile(mtime=0)` and a `tarfile.add(..., filter=...)` callback).
  Verified standalone: two `--stable` runs of unchanged content now produce byte-identical
  archives (`cmp` on the raw bytes, not just the extracted content).
- `admin_interface` gains `get_revisions_targets()`, declaring its own `theme` target for
  `ophix-revisions` (if installed) to discover at runtime — no separate registration
  needed anywhere else.

## 2026.07.12.02

- Migration `0002_remove_theme_placeholder_fields` no longer uses raw SQL — it used
  MySQL/MariaDB backtick-quoted identifiers (`` `admin_interface_theme` ``), which are a
  syntax error on Postgres, Oracle, SQL Server, and CockroachDB. Replaced with a portable
  `RunPython` that uses Django's own `SchemaEditor.remove_field()` plus a backend-agnostic
  introspection check (`connection.introspection.get_table_description()`), so the same
  idempotent "only drop the column if it's actually there" behaviour now works on every
  supported engine, not just MariaDB. Found while scoping out multi-engine Docker-based
  testing for the `ophix-dbengine-*` plugins.

## 2026.07.12.01

- #30: Nav sidebar width reduced from 360px to 300px. Updated in lockstep across
  `nav-sidebar.css`, `sticky-form-controls.css` (sticky pagination/submit-row widths),
  and `rtl.css` (mirrored values, including a derived `-260px` for a padding-offset
  value that isn't independently verified — RTL is not in active use anywhere in the
  fleet).

## 2026.06.11.01

- Added `css_body_background_color` field (with dark-mode pair) to the Theme model —
  controls the overall page background for all admin pages. Leave blank to inherit Django's
  default. Placed at the top of the Body Text section in the theme editor.
  Applied via `body.admin-interface { background: var(--admin-interface-body-background-color, var(--body-bg)); }`.
  Error pages use this field for `--ep-body-bg`; when blank they fall back to
  `css_module_background_color` (previous behaviour unchanged).
- Auto-dismiss for message banners: reads `window.OPHIX_AUTOHIDE` config (emitted by
  `ophix-admin-settings` when enabled) and auto-removes success and info banners after
  the configured delay. Hover cancels the timer. Errors and warnings are never auto-hidden.
  Dismiss button (×) behaviour is unchanged.

- Added `generate_error_pages` management command — renders static HTML error pages
  (400, 403, 404, 500, 503) with the active theme's colors baked in as inline CSS
  variables. Output goes to `INSTALL_DIR/static/error_pages/`. Dark mode uses
  `@media (prefers-color-scheme: dark)` with per-color overrides from the theme's
  dark-mode fields. Run standalone or called automatically by `run_install`.
- `post_save` signal on `Theme`: when an active theme is saved and
  `INSTALL_DIR/static/error_pages/` already exists, `generate_error_pages` runs
  automatically so error pages stay in sync with theme changes. Skips silently on
  fresh installs before `run_install` has created the directory.
- Fixed `ThemeAdmin.response_change` missing `_popup` guard — when a theme was opened
  in a Magnific Popup and saved, the response redirected to the changelist instead of
  returning Django's popup-closing response. Added `if "_popup" in request.POST: return
  super().response_change(request, obj)` as the first line of the override.
- Fixed `0002_remove_theme_placeholder_fields` migration idempotency — replaced plain
  `RemoveField` operations with `SeparateDatabaseAndState` using
  `ALTER TABLE ... DROP COLUMN IF EXISTS` SQL, so the migration is safe to re-run on
  servers where the columns were already dropped by an earlier cleanup script.
- `dismiss.js` moved to a static file loaded in `{% block extrastyle %}` in
  `base_site.html` — previously in `{% block extrascript %}` which is overridden by
  `change_form.html`.
- Test message insertion now correctly targets the parent wrapper sibling of `#content`.
- `.deletelink` excluded from the link hover underline rule in `widgets.css`.

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
