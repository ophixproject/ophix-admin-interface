from django.contrib import admin
from django.forms import ClearableFileInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from admin_interface.models import Theme


class ImagePreviewWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, "url"):
            output = format_html(
                '<div class="image-preview">'
                '<img src="{}" alt="" style="max-height:80px;max-width:200px;'
                'display:block;margin-bottom:6px;border:1px solid #ccc;border-radius:3px;">'
                "</div>{}",
                value.url,
                output,
            )
        return output


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
                    "logo_color",
                    "logo_visible",
                ),
            },
        ),
        (_("Favicon"), {"classes": ("wide",), "fields": ("favicon",)}),
        (
            _("Title"),
            {
                "classes": ("wide",),
                "fields": (
                    "title_color",
                ),
            },
        ),
        (
            _("Header"),
            {
                "classes": ("wide",),
                "fields": (
                    "css_header_background_color",
                    "css_header_text_color",
                    "css_header_link_color",
                    "css_header_link_hover_color",
                    "env_color",
                ),
                "description": _(
                    "env_color is the colour of the environment badge "
                    "(e.g. Production / Staging). The badge text and visibility "
                    "are configured in Server Settings."
                ),
            },
        ),
        (
            _("Breadcrumbs / Module headers"),
            {
                "classes": ("wide",),
                "fields": (
                    "css_module_background_color",
                    "css_module_background_selected_color",
                    "css_module_text_color",
                    "css_module_link_color",
                    "css_module_link_selected_color",
                    "css_module_link_hover_color",
                    "css_module_border_radius",
                ),
            },
        ),
        (
            _("Body Text"),
            {
                "classes": ("wide",),
                "fields": (
                    "css_body_font_family",
                    "css_body_font_size",
                    "css_generic_link_color",
                    "css_generic_link_hover_color",
                    "css_generic_link_active_color",
                ),
            },
        ),
        (
            _("Buttons"),
            {
                "classes": ("wide",),
                "fields": (
                    "css_save_button_background_color",
                    "css_save_button_background_hover_color",
                    "css_save_button_text_color",
                    "css_button_font_size",
                    "css_button_border_radius",
                ),
            },
        ),
        (
            _("Alert Buttons"),
            {
                "classes": ("wide",),
                "fields": (
                    "css_delete_button_background_color",
                    "css_delete_button_background_hover_color",
                    "css_delete_button_text_color",
                ),
            },
        ),
        (
            _("Notification Colors"),
            {
                "classes": ("wide",),
                "fields": (
                    "css_success_color",
                    "css_warning_color",
                    "css_muted_color",
                    "css_alert_color",
                ),
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
                    "related_modal_background_color",
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

    class Media:
        js = ("admin_interface/colorfield/colorfield-swatch.js",)
