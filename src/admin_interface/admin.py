from django.contrib import admin
from django.forms import ClearableFileInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from admin_interface.models import Theme

_DARK_HINT = _("Check the box to override this colour in dark mode. Leave the colour blank to fall back to the light value.")


class ImagePreviewWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        file_input = super().render(name, value, attrs, renderer)
        if name == "logo":
            if value and hasattr(value, "url"):
                preview = format_html(
                    '<div class="logo-preview-container" id="logo-preview-container">'
                    '<img id="logo-preview-img" src="{}" alt="" class="logo-preview-img">'
                    "</div>",
                    value.url,
                )
            else:
                preview = mark_safe(
                    '<div class="logo-preview-container" id="logo-preview-container">'
                    '<img id="logo-preview-img" src="" alt="" class="logo-preview-img" style="display:none">'
                    "</div>"
                )
        elif value and hasattr(value, "url"):
            preview = format_html(
                '<div class="image-preview">'
                '<img src="{}" alt="" style="max-height:80px;max-width:200px;">'
                "</div>",
                value.url,
            )
        else:
            preview = mark_safe("")
        return format_html(
            '{}<div class="file-input-wrap">{}</div>',
            preview,
            file_input,
        )


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
    )
    list_editable = ("active",)
    actions = None
    list_per_page = 100
    show_full_result_count = False

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ("logo", "favicon"):
            kwargs["widget"] = ImagePreviewWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "active",
                ),
            },
        ),
        (
            _("Logo"),
            {
                "classes": ("wide",),
                "fields": (
                    "logo",
                    "logo_max_width",
                    "logo_max_height",
                    ("logo_color", "logo_color_dark_use", "logo_color_dark"),
                    "logo_visible",
                ),
                "description": _DARK_HINT,
            },
        ),
        (_("Favicon"), {"classes": ("wide",), "fields": ("favicon",)}),
        (
            _("Title"),
            {
                "classes": ("wide",),
                "fields": (
                    ("title_color", "title_color_dark_use", "title_color_dark"),
                ),
                "description": _DARK_HINT,
            },
        ),
        (
            _("Header"),
            {
                "classes": ("wide",),
                "fields": (
                    ("css_header_background_color", "css_header_background_color_dark_use", "css_header_background_color_dark"),
                    ("css_header_text_color", "css_header_text_color_dark_use", "css_header_text_color_dark"),
                    ("css_header_link_color", "css_header_link_color_dark_use", "css_header_link_color_dark"),
                    ("css_header_link_hover_color", "css_header_link_hover_color_dark_use", "css_header_link_hover_color_dark"),
                    ("env_color", "env_color_dark_use", "env_color_dark"),
                ),
                "description": _(
                    "env_color is the colour of the environment badge "
                    "(e.g. Production / Staging). The badge text and visibility "
                    "are configured in Server Settings. — "
                ) + str(_DARK_HINT),
            },
        ),
        (
            _("Breadcrumbs / Module headers"),
            {
                "classes": ("wide",),
                "fields": (
                    ("css_module_background_color", "css_module_background_color_dark_use", "css_module_background_color_dark"),
                    ("css_module_background_selected_color", "css_module_background_selected_color_dark_use", "css_module_background_selected_color_dark"),
                    ("css_module_text_color", "css_module_text_color_dark_use", "css_module_text_color_dark"),
                    ("css_module_link_color", "css_module_link_color_dark_use", "css_module_link_color_dark"),
                    ("css_module_link_selected_color", "css_module_link_selected_color_dark_use", "css_module_link_selected_color_dark"),
                    ("css_module_link_hover_color", "css_module_link_hover_color_dark_use", "css_module_link_hover_color_dark"),
                    "css_module_border_radius",
                ),
                "description": _DARK_HINT,
            },
        ),
        (
            _("Body Text"),
            {
                "classes": ("wide",),
                "fields": (
                    "css_body_font_family",
                    "css_body_font_size",
                    ("css_generic_link_color", "css_generic_link_color_dark_use", "css_generic_link_color_dark"),
                    ("css_generic_link_hover_color", "css_generic_link_hover_color_dark_use", "css_generic_link_hover_color_dark"),
                    ("css_generic_link_active_color", "css_generic_link_active_color_dark_use", "css_generic_link_active_color_dark"),
                ),
                "description": _DARK_HINT,
            },
        ),
        (
            _("Buttons"),
            {
                "classes": ("wide",),
                "fields": (
                    ("css_save_button_background_color", "css_save_button_background_color_dark_use", "css_save_button_background_color_dark"),
                    ("css_save_button_background_hover_color", "css_save_button_background_hover_color_dark_use", "css_save_button_background_hover_color_dark"),
                    ("css_save_button_text_color", "css_save_button_text_color_dark_use", "css_save_button_text_color_dark"),
                    "css_button_font_size",
                    "css_button_border_radius",
                ),
                "description": _DARK_HINT,
            },
        ),
        (
            _("Alert Buttons"),
            {
                "classes": ("wide",),
                "fields": (
                    ("css_delete_button_background_color", "css_delete_button_background_color_dark_use", "css_delete_button_background_color_dark"),
                    ("css_delete_button_background_hover_color", "css_delete_button_background_hover_color_dark_use", "css_delete_button_background_hover_color_dark"),
                    ("css_delete_button_text_color", "css_delete_button_text_color_dark_use", "css_delete_button_text_color_dark"),
                ),
                "description": _DARK_HINT,
            },
        ),
        (
            _("Notification Colors"),
            {
                "classes": ("wide",),
                "fields": (
                    ("css_success_color", "css_success_color_dark_use", "css_success_color_dark"),
                    ("css_warning_color", "css_warning_color_dark_use", "css_warning_color_dark"),
                    ("css_muted_color", "css_muted_color_dark_use", "css_muted_color_dark"),
                    ("css_alert_color", "css_alert_color_dark_use", "css_alert_color_dark"),
                ),
                "description": _DARK_HINT,
            },
        ),
        (
            _("Navigation Bar"),
            {
                "classes": ("wide",),
                "fields": ("foldable_apps",),
            },
        ),
        (
            _("Related Modal"),
            {
                "classes": ("wide",),
                "description": _(
                    "The background overlay dims the page behind the modal popup. "
                    "Background overlay colour and opacity control its appearance."
                ),
                "fields": (
                    "related_modal_active",
                    ("related_modal_background_color", "related_modal_background_color_dark_use", "related_modal_background_color_dark"),
                    "related_modal_background_opacity",
                    "related_modal_rounded_corners",
                    "related_modal_close_button_visible",
                ),
            },
        ),
        (
            _("Form Controls"),
            {
                "classes": ("wide",),
                "fields": (
                    "form_actions_sticky",
                    "form_submit_sticky",
                    "form_pagination_sticky",
                ),
            },
        ),
        (
            _("List Filter"),
            {
                "classes": ("wide",),
                "fields": (
                    "list_filter_highlight",
                    "list_filter_dropdown",
                    "list_filter_sticky",
                    "list_filter_removal_links",
                ),
            },
        ),
        (
            _("Change Form"),
            {
                "classes": ("wide",),
                "fields": (
                    "show_fieldsets_as_tabs",
                    "show_inlines_as_tabs",
                ),
            },
        ),
        (
            _("Inlines"),
            {
                "classes": ("wide",),
                "fields": (
                    "collapsible_stacked_inlines",
                    "collapsible_stacked_inlines_collapsed",
                    "collapsible_tabular_inlines",
                    "collapsible_tabular_inlines_collapsed",
                ),
            },
        ),
        (
            _("Recent Actions"),
            {
                "classes": ("wide",),
                "fields": ("recent_actions_visible",),
            },
        ),
    )

    save_on_top = True
    change_form_template = "admin/admin_interface/theme/change_form.html"

    class Media:
        css = {
            "all": ("admin_interface/css/theme-editor.css",),
        }
        js = (
            "admin_interface/colorfield/colorfield-swatch.js",
            "admin_interface/js/dark-toggle.js",
            "admin_interface/js/logo-preview.js",
            "admin_interface/js/theme-sections.js",
        )
