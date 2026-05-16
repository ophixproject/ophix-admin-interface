import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

_VAR_NAME_RE = re.compile(r'^--[a-zA-Z][a-zA-Z0-9-]*$')

# Characters that would break out of a CSS declaration context.
_VALUE_FORBIDDEN = re.compile(r'[;{}]', re.IGNORECASE)
# CSS functions that can load external resources or execute code.
_VALUE_FORBIDDEN_FUNCS = re.compile(r'\b(url|expression|calc|var|env|attr)\s*\(', re.IGNORECASE)


def validate_custom_css_vars(value):
    """Validate a dict of CSS custom property name → value pairs."""
    if not isinstance(value, dict):
        raise ValidationError(_("Must be a JSON object mapping CSS variable names to values."))

    errors = []
    for key, val in value.items():
        if not _VAR_NAME_RE.match(key):
            errors.append(
                _("Invalid CSS variable name '%(key)s'. "
                  "Must start with '--' followed by a letter, then letters, digits, or hyphens.")
                % {"key": key}
            )
        if not isinstance(val, str):
            errors.append(_("Value for '%(key)s' must be a string.") % {"key": key})
            continue
        if _VALUE_FORBIDDEN.search(val):
            errors.append(
                _("Value for '%(key)s' contains forbidden characters (; { }).")
                % {"key": key}
            )
        if _VALUE_FORBIDDEN_FUNCS.search(val):
            errors.append(
                _("Value for '%(key)s' contains a forbidden CSS function.")
                % {"key": key}
            )

    if errors:
        raise ValidationError(errors)
