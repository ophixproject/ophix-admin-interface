import os
import shutil

from django.conf import settings
from django.contrib import admin
from django.core.files.uploadedfile import UploadedFile
from django.forms import ClearableFileInput
from django.contrib.messages import SUCCESS as MSG_SUCCESS
from django.http import HttpResponseRedirect
from django.urls import reverse
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
                    "logo_vertical_offset",
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
                    "title_font_size",
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
                ),
                "description": _DARK_HINT,
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
            _("Message Banners"),
            {
                "classes": ("wide",),
                "fields": (
                    ("css_message_success_bg", "css_message_success_bg_dark_use", "css_message_success_bg_dark"),
                    ("css_message_success_text", "css_message_success_text_dark_use", "css_message_success_text_dark"),
                    ("css_message_warning_bg", "css_message_warning_bg_dark_use", "css_message_warning_bg_dark"),
                    ("css_message_warning_text", "css_message_warning_text_dark_use", "css_message_warning_text_dark"),
                    ("css_message_error_bg", "css_message_error_bg_dark_use", "css_message_error_bg_dark"),
                    ("css_message_error_text", "css_message_error_text_dark_use", "css_message_error_text_dark"),
                    ("css_message_info_bg", "css_message_info_bg_dark_use", "css_message_info_bg_dark"),
                    ("css_message_info_text", "css_message_info_text_dark_use", "css_message_info_text_dark"),
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

    def _clean_save_msg(self, verb):
        return _("%(verbose_name)s %(verb)s successfully.") % {
            "verbose_name": self.model._meta.verbose_name.capitalize(),
            "verb": verb,
        }

    def response_add(self, request, obj, post_url_continue=None):
        if "_popup" in request.POST:
            return super().response_add(request, obj, post_url_continue)
        self.message_user(request, self._clean_save_msg("added"), MSG_SUCCESS)
        opts = self.model._meta
        if "_continue" in request.POST:
            return HttpResponseRedirect(
                reverse(
                    f"admin:{opts.app_label}_{opts.model_name}_change",
                    args=[obj.pk],
                    current_app=self.admin_site.name,
                )
            )
        if "_addanother" in request.POST:
            return HttpResponseRedirect(
                reverse(
                    f"admin:{opts.app_label}_{opts.model_name}_add",
                    current_app=self.admin_site.name,
                )
            )
        return HttpResponseRedirect(
            reverse(
                f"admin:{opts.app_label}_{opts.model_name}_changelist",
                current_app=self.admin_site.name,
            )
        )

    def response_change(self, request, obj):
        if "_popup" in request.POST:
            return super().response_change(request, obj)
        self.message_user(request, self._clean_save_msg("saved"), MSG_SUCCESS)
        if "_continue" in request.POST:
            return HttpResponseRedirect(request.path)
        return HttpResponseRedirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist",
                current_app=self.admin_site.name,
            )
        )

    def save_model(self, request, obj, form, change):
        if not change:
            super().save_model(request, obj, form, change)
            return

        old = Theme.objects.get(pk=obj.pk)
        old_name = old.name
        new_name = obj.name
        renamed = old_name != new_name

        logo_is_new = isinstance(form.cleaned_data.get("logo"), UploadedFile)
        logo_is_cleared = form.cleaned_data.get("logo") is False
        fav_is_new = isinstance(form.cleaned_data.get("favicon"), UploadedFile)
        fav_is_cleared = form.cleaned_data.get("favicon") is False

        media_root = settings.MEDIA_ROOT
        old_base = os.path.join(media_root, "admin-interface", "themes", old_name)
        new_base = os.path.join(media_root, "admin-interface", "themes", new_name)

        _slots = (
            ("logo", "logo", logo_is_new, logo_is_cleared),
            ("favicon", "favicon", fav_is_new, fav_is_cleared),
        )

        if renamed:
            os.makedirs(new_base, exist_ok=True)
            for subdir, field, is_new, is_cleared in _slots:
                old_dir = os.path.join(old_base, subdir)
                new_dir = os.path.join(new_base, subdir)
                old_field = getattr(old, field)
                if is_new or is_cleared:
                    # Old subfolder replaced or cleared — remove it; new upload lands in new_base
                    shutil.rmtree(old_dir, ignore_errors=True)
                elif old_field and os.path.exists(old_dir):
                    # Keeping the same file — move folder and update stored path
                    shutil.move(old_dir, new_dir)
                    new_path = old_field.name.replace(
                        "admin-interface/themes/{}/{}/".format(old_name, subdir),
                        "admin-interface/themes/{}/{}/".format(new_name, subdir),
                    )
                    getattr(obj, field).name = new_path
        else:
            for subdir, field, is_new, is_cleared in _slots:
                old_field = getattr(old, field)
                if (is_new or is_cleared) and old_field:
                    shutil.rmtree(os.path.join(old_base, subdir), ignore_errors=True)

        super().save_model(request, obj, form, change)

        # After successful save, remove the old base folder (renamed away from it)
        if renamed and os.path.exists(old_base):
            shutil.rmtree(old_base, ignore_errors=True)

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
