# ophix-admin-interface

The admin interface foundation for [Ophix Project](https://ophix.io) servers.

A fork of [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface), extended for the Ophix platform.

## What this package provides

- Full theme management: per-server colour schemes, logos, and branding via the Django admin UI
- Extended CSS custom properties for consistent styling across Ophix domain plugins
- Namespaced static media to prevent collisions between installed plugins
- `install_bundled_theme()` API used by Ophix theme packages to ship themes as pip packages
- Air-gap safe — all assets are bundled, no CDN dependencies at runtime

## Installation

```bash
pip install ophix-admin-interface
```

This package is a declared dependency of `ophix-server-base` and is installed automatically
as part of any Ophix server deployment. Operators do not normally need to install it directly.

## Theme packages

Ophix theme packages (`ophix-theme-midnight`, `ophix-theme-imago`, etc.) depend on this
package and use `install_bundled_theme()` to register themes on `post_migrate`. Themes
install inactive; the operator activates one via the admin UI or the `set_theme` management
command.

## License

MIT
