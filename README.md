# ophix-admin-interface

**Make the admin UI look like yours** — customisable branding for every [Ophix](https://ophix.io) server, built on [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface).

Nobody wants to run their infrastructure through something that visibly looks like generic open-source software. `ophix-admin-interface` makes full white-labelling a first-class, no-code feature: set your colours and logo through the admin UI itself, and every server looks unmistakably like it belongs to you.

This package is automatically included in every Ophix server, no need to separately install it.

## What this package provides

- Full theme management: per-server colour schemes, logos, and branding via the Django admin UI
- Extended CSS custom properties for consistent styling across Ophix domain plugins
- Namespaced static media to prevent collisions between installed plugins
- `install_bundled_theme()` API used by Ophix theme packages to ship themes as pip packages
- Air-gap safe — all assets are bundled, no CDN dependencies at runtime

## Installation

Installed automatically with `ophix-server-base`. To install explicitly:

```bash
pip install ophix-admin-interface
```

## Theme packages

Ophix theme packages (`ophix-theme-midnight`, `ophix-theme-ocean`, etc.) depend on this
package and use `install_bundled_theme()` to register themes on `post_migrate`. Themes
install inactive; the operator activates one via the admin UI or the `set_theme` management
command.

## License

MIT
