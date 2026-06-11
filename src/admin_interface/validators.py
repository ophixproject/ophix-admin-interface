"""
admin_interface.validators
~~~~~~~~~~~~~~~~~~~~~~~~~~
Security validators for Theme model fields that are emitted into CSS.

All fields whose values reach a <style> block are validated here.  Django's
template auto-escaping does not apply inside <style> tags, so we use an
allowlist (Perl-taint) approach: define exactly what characters are permitted
and reject everything else, regardless of whether the submitted value would
produce valid CSS.  The goal is containment, not CSS syntax validation.

Five validator functions, grouped by what they accept:

    validate_css_color       – #RGB / #RRGGBB / #RRGGBBAA hex only
    validate_css_dimension   – a positive number followed by a CSS unit
    validate_css_font_family – Unicode letters/digits, commas, hyphens, quotes
    validate_theme_name      – letters, digits, spaces, hyphens (no path chars)
    validate_server_title    – printable text minus HTML/CSS injection chars

Entry points that bypass Django form validation (management commands, loaddata,
install_bundled_theme) must call check_theme_json_fields() on the raw JSON
fields dict before touching the database.
"""

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------
# Compiled patterns
# ---------------------------------------------------------------------------

# Hex colour: #RGB, #RGBA, #RRGGBB, or #RRGGBBAA — nothing else.
_HEX_COLOR_RE = re.compile(
    r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$"
)

# Single CSS dimension: bare 0, or a positive decimal number + an explicit unit.
_CSS_DIMENSION_RE = re.compile(
    r"^0$|^\d+(\.\d+)?(px|rem|em|%|vw|vh|pt|ch|ex|dvh|dvw|svh|svw)$"
)

# Font family: Unicode word chars, spaces, commas, hyphens, periods, quotes.
# Denies { } ; < > / \ @ ! * ( ) and anything else not in this set.
_CSS_FONT_FAMILY_RE = re.compile(r"^[\w\s,\-\.\'\"]+$", re.UNICODE)

# Theme name: Unicode letters, digits, spaces, hyphens. No dots or slashes
# (dots could form .. traversal in the upload_to path).
_THEME_NAME_RE = re.compile(r"^[\w\s\-]+$", re.UNICODE)

# Server title: everything except the handful of chars that enable HTML/CSS
# injection: { } < > ; \
_SERVER_TITLE_RE = re.compile(r"^[^{}<>;\\]*$", re.UNICODE)

# Environment name: strict allowlist — letters, digits, spaces, hyphens only.
_ENV_NAME_RE = re.compile(r"^[\w\s\-]*$", re.UNICODE)

# ---------------------------------------------------------------------------
# Error messages
# ---------------------------------------------------------------------------

_COLOR_MSG = _(
    "Enter a hex colour code — e.g. #0096c7 (6 digits) or #09c (3 digits). "
    "Named colours and CSS functions are not accepted."
)
_DIMENSION_MSG = _(
    "Enter a number with a CSS unit — e.g. 14px, 1.5rem, 50%, or 0. "
    "Only a single value is accepted."
)
_FONT_FAMILY_MSG = _(
    "Font family contains one or more characters that are not allowed. "
    "Use font names, commas for fallbacks, and quotes for multi-word names — "
    'e.g. "Segoe UI", Arial, sans-serif. '
    "Characters like { } ; < > are not permitted."
)
_THEME_NAME_MSG = _(
    "Theme name may only contain letters, numbers, spaces, and hyphens."
)
_SERVER_TITLE_MSG = _(
    "Server title contains invalid characters. "
    "Use letters, numbers, spaces, and standard punctuation."
)
_ENV_NAME_MSG = _(
    "Environment name may only contain letters, numbers, spaces, and hyphens — "
    "e.g. Production, Staging, Dev-EU."
)

# ---------------------------------------------------------------------------
# Validator functions
# ---------------------------------------------------------------------------


def validate_css_color(value):
    """Accept only empty string or a hex colour (#RGB / #RRGGBB / #RRGGBBAA).

    Leading and trailing whitespace is stripped before checking — a field that
    contains only spaces is treated as blank (allowed), and a value like
    ' #0096c7 ' passes the same as '#0096c7'.
    """
    if not value:
        return
    if not _HEX_COLOR_RE.match(value.strip()):
        raise ValidationError(_COLOR_MSG)


def validate_css_dimension(value):
    """Accept only empty string, 0, or a positive decimal number + CSS unit."""
    if not value:
        return
    if not _CSS_DIMENSION_RE.match(value):
        raise ValidationError(_DIMENSION_MSG)


def validate_css_font_family(value):
    """Accept only characters safe in a CSS font-family value."""
    if not value:
        return
    if not _CSS_FONT_FAMILY_RE.match(value):
        raise ValidationError(_FONT_FAMILY_MSG)


def validate_theme_name(value):
    """Accept only letters, digits, spaces, and hyphens."""
    if not value:
        return
    if not _THEME_NAME_RE.match(value):
        raise ValidationError(_THEME_NAME_MSG)


def validate_server_title(value):
    """Accept printable text; deny characters that enable HTML/CSS injection."""
    if not value:
        return
    if not _SERVER_TITLE_RE.match(value):
        raise ValidationError(_SERVER_TITLE_MSG)


def validate_env_name(value):
    """Accept only letters, digits, spaces, and hyphens."""
    if not value:
        return
    if not _ENV_NAME_RE.match(value):
        raise ValidationError(_ENV_NAME_MSG)


# ---------------------------------------------------------------------------
# Field inventories (shared by Theme.clean() and management command pre-validation)
# ---------------------------------------------------------------------------

# Every ColorField on the Theme model, in model definition order.
THEME_COLOR_FIELDS = (
    "title_color",
    "title_color_dark",
    "logo_color",
    "logo_color_dark",
    "css_header_background_color",
    "css_header_background_color_dark",
    "css_header_text_color",
    "css_header_text_color_dark",
    "css_header_link_color",
    "css_header_link_color_dark",
    "css_header_link_hover_color",
    "css_header_link_hover_color_dark",
    "css_module_background_color",
    "css_module_background_color_dark",
    "css_module_background_selected_color",
    "css_module_background_selected_color_dark",
    "css_module_text_color",
    "css_module_text_color_dark",
    "css_module_link_color",
    "css_module_link_color_dark",
    "css_module_link_selected_color",
    "css_module_link_selected_color_dark",
    "css_module_link_hover_color",
    "css_module_link_hover_color_dark",
    "css_body_background_color",
    "css_body_background_color_dark",
    "css_generic_link_color",
    "css_generic_link_color_dark",
    "css_generic_link_hover_color",
    "css_generic_link_hover_color_dark",
    "css_generic_link_active_color",
    "css_generic_link_active_color_dark",
    "css_save_button_background_color",
    "css_save_button_background_color_dark",
    "css_save_button_background_hover_color",
    "css_save_button_background_hover_color_dark",
    "css_save_button_text_color",
    "css_save_button_text_color_dark",
    "css_delete_button_background_color",
    "css_delete_button_background_color_dark",
    "css_delete_button_background_hover_color",
    "css_delete_button_background_hover_color_dark",
    "css_delete_button_text_color",
    "css_delete_button_text_color_dark",
    "css_success_color",
    "css_success_color_dark",
    "css_warning_color",
    "css_warning_color_dark",
    "css_muted_color",
    "css_muted_color_dark",
    "css_alert_color",
    "css_alert_color_dark",
    "css_message_success_bg",
    "css_message_success_bg_dark",
    "css_message_warning_bg",
    "css_message_warning_bg_dark",
    "css_message_error_bg",
    "css_message_error_bg_dark",
    "css_message_info_bg",
    "css_message_info_bg_dark",
    "css_message_success_text",
    "css_message_success_text_dark",
    "css_message_warning_text",
    "css_message_warning_text_dark",
    "css_message_error_text",
    "css_message_error_text_dark",
    "css_message_info_text",
    "css_message_info_text_dark",
    "related_modal_background_color",
    "related_modal_background_color_dark",
)

# Every CharField on the Theme model that holds a CSS dimension value.
THEME_DIMENSION_FIELDS = (
    "title_font_size",
    "css_module_border_radius",
    "css_body_font_size",
    "css_button_font_size",
    "css_button_border_radius",
)

# ---------------------------------------------------------------------------
# Management command helper
# ---------------------------------------------------------------------------


def check_theme_json_fields(theme_name, fields):
    """
    Validate the 'fields' dict from a theme.json object before database write.

    Args:
        theme_name: the resolved theme name (after any --rename was applied).
        fields:     the 'fields' dict from one theme.json entry.

    Returns:
        A list of (field_name, display_value, error_message) tuples for every
        field that failed validation.  An empty list means all fields passed.
    """
    problems = []

    def _check(field_name, validator, normalize=False):
        raw = fields.get(field_name)
        value = str(raw) if raw is not None else ""
        if normalize:
            value = value.strip()
            fields[field_name] = value  # write back so loaddata saves the clean value
        try:
            validator(value)
        except ValidationError as exc:
            display = value if len(value) <= 80 else value[:77] + "..."
            message = "; ".join(str(m) for m in exc.messages)
            problems.append((field_name, display, message))

    for field_name in THEME_COLOR_FIELDS:
        _check(field_name, validate_css_color, normalize=True)

    for field_name in THEME_DIMENSION_FIELDS:
        _check(field_name, validate_css_dimension)

    _check("css_body_font_family", validate_css_font_family)
    _check("name", validate_theme_name)

    return problems
