import shutil
from pathlib import Path

from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from .cache import del_cached_active_theme


def _logo_upload_to(instance, filename):
    return "admin-interface/themes/{}/logo/{}".format(instance.name, filename)


def _logo_dark_upload_to(instance, filename):
    # Retained for migration 0035 compatibility — field removed in 0036.
    return "admin-interface/themes/{}/logo_dark/{}".format(instance.name, filename)


def _favicon_upload_to(instance, filename):
    return "admin-interface/themes/{}/favicon/{}".format(instance.name, filename)


class ThemeQuerySet(models.QuerySet):
    def get_active(self):
        objs_active_qs = self.filter(active=True)
        objs_active_ls = list(objs_active_qs)
        objs_active_count = len(objs_active_ls)

        if objs_active_count == 0:
            obj = self.all().first()
            if obj:
                obj.set_active()
            else:
                obj = self.create()

        elif objs_active_count == 1:
            obj = objs_active_ls[0]

        elif objs_active_count > 1:
            obj = objs_active_ls[-1]
            obj.set_active()

        return obj


class Theme(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        default="",
        verbose_name=_("name"),
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
    )

    title_font_size = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text=_("e.g. 1.5rem, 24px · Leave blank to use the theme default."),
        verbose_name=_("font size"),
    )
    title_color = ColorField(
        blank=True,
        default="#fffdfa",
        help_text=_("Colour of the title text in the header bar"),
        max_length=10,
        verbose_name=_("color"),
    )
    title_color_dark_use = models.BooleanField(
        default=False,
        verbose_name=_("dark?"),
    )
    title_color_dark = ColorField(
        blank=True,
        default="",
        max_length=10,
        verbose_name=_("dark"),
    )
    logo = models.FileField(
        upload_to=_logo_upload_to,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["gif", "jpg", "jpeg", "png", "svg"]
            )
        ],
        help_text=_("Leave blank to use the default Django logo"),
        verbose_name=_("logo"),
    )
    logo_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Tint applied to the logo SVG; white shows the logo unchanged"),
        max_length=10,
        verbose_name=_("color"),
    )
    logo_color_dark_use = models.BooleanField(
        default=False,
        verbose_name=_("dark?"),
    )
    logo_color_dark = ColorField(
        blank=True,
        default="",
        max_length=10,
        verbose_name=_("dark"),
    )
    logo_max_width = models.PositiveSmallIntegerField(
        blank=True,
        default=400,
        verbose_name=_("max width"),
    )
    logo_max_height = models.PositiveSmallIntegerField(
        blank=True,
        default=100,
        verbose_name=_("max height"),
    )
    logo_visible = models.BooleanField(
        default=True,
        verbose_name=_("visible"),
    )
    logo_vertical_offset = models.SmallIntegerField(
        default=0,
        verbose_name=_("vertical offset"),
        help_text=_("Pixels to shift the logo up (positive) or down (negative) relative to its natural position."),
    )
    favicon = models.FileField(
        upload_to=_favicon_upload_to,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["gif", "ico", "jpg", "jpeg", "png", "svg"]
            )
        ],
        help_text=_("(.ico|.png|.gif - 16x16|32x32 px)"),
        verbose_name=_("favicon"),
    )

    css_header_background_color = ColorField(
        blank=True,
        default="#0c0c0d",
        help_text=_("Background colour of the top header bar"),
        max_length=10,
        verbose_name=_("background color"),
    )
    css_header_background_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_header_background_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_header_text_color = ColorField(
        blank=True,
        default="#fffdfa",
        help_text=_("Colour of plain text in the header bar"),
        max_length=10,
        verbose_name=_("text color"),
    )
    css_header_text_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_header_text_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_header_link_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Colour of navigation links in the header bar"),
        max_length=10,
        verbose_name=_("link color"),
    )
    css_header_link_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_header_link_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_header_link_hover_color = ColorField(
        blank=True,
        default="#ade9f4",
        help_text=_("Header link colour on hover"),
        max_length=10,
        verbose_name=_("link hover color"),
    )
    css_header_link_hover_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_header_link_hover_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_module_background_color = ColorField(
        blank=True,
        default="#0c0c0d",
        help_text=_("Background colour of section header bars (module titles)"),
        max_length=10,
        verbose_name=_("background color"),
    )
    css_module_background_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_module_background_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_module_background_selected_color = ColorField(
        blank=True,
        default="#f1fcfe",
        help_text=_("Background colour of selected / highlighted rows"),
        max_length=10,
        verbose_name=_("background selected color"),
    )
    css_module_background_selected_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_module_background_selected_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_module_text_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Text colour inside section header bars"),
        max_length=10,
        verbose_name=_("text color"),
    )
    css_module_text_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_module_text_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_module_link_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Link colour inside section header bars"),
        max_length=10,
        verbose_name=_("link color"),
    )
    css_module_link_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_module_link_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_module_link_selected_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Link colour for selected items inside section header bars"),
        max_length=10,
        verbose_name=_("link selected color"),
    )
    css_module_link_selected_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_module_link_selected_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_module_link_hover_color = ColorField(
        blank=True,
        default="#ade9f4",
        help_text=_("Link colour on hover inside section header bars"),
        max_length=10,
        verbose_name=_("link hover color"),
    )
    css_module_link_hover_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_module_link_hover_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_module_border_radius = models.CharField(
        max_length=20,
        blank=True,
        default="0",
        help_text=_("e.g. 4px · 0px · 0.5rem"),
        verbose_name=_("border radius"),
    )
    css_tab_border_radius = models.CharField(
        max_length=20,
        blank=True,
        default="0",
        help_text=_("e.g. 4px · 0px · 0.5rem. Controls tab and nav sidebar toggle handle border-radius independently of modules."),
        verbose_name=_("tab border radius"),
    )

    css_body_background_color = ColorField(
        blank=True,
        default="",
        help_text=_("Overall page background colour for all admin pages. Leave blank to use the browser default."),
        max_length=10,
        verbose_name=_("background color"),
    )
    css_body_background_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_body_background_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_body_font_family = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text=_("e.g. Arial, sans-serif · Leave blank to use the browser default."),
        verbose_name=_("font family"),
    )
    css_body_font_size = models.CharField(
        max_length=20,
        blank=True,
        default="14px",
        help_text=_("e.g. 14px · 0.875rem · Leave blank to fall back to the "
                     "browser default, which varies inconsistently page to page."),
        verbose_name=_("font size"),
    )
    css_body_text_color = ColorField(
        blank=True,
        default="",
        help_text=_("Body text colour. Leave blank to use the browser default."),
        max_length=10,
        verbose_name=_("text color"),
    )
    css_body_text_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_body_text_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_generic_link_color = ColorField(
        blank=True,
        default="#0096c7",
        help_text=_("Default link colour in page content"),
        max_length=10,
        verbose_name=_("link color"),
    )
    css_generic_link_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_generic_link_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_generic_link_hover_color = ColorField(
        blank=True,
        default="#023e8a",
        help_text=_("Page content link colour on hover"),
        max_length=10,
        verbose_name=_("link hover color"),
    )
    css_generic_link_hover_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_generic_link_hover_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_generic_link_active_color = ColorField(
        blank=True,
        default="#48cae4",
        help_text=_("Page content link colour when active / pressed"),
        max_length=10,
        verbose_name=_("link active color"),
    )
    css_generic_link_active_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_generic_link_active_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_save_button_background_color = ColorField(
        blank=True,
        default="#0096c7",
        help_text=_("Background colour of Save / primary action buttons"),
        max_length=10,
        verbose_name=_("background color"),
    )
    css_save_button_background_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_save_button_background_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_save_button_background_hover_color = ColorField(
        blank=True,
        default="#023e8a",
        help_text=_("Save button background colour on hover"),
        max_length=10,
        verbose_name=_("background hover color"),
    )
    css_save_button_background_hover_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_save_button_background_hover_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_save_button_text_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Text colour on Save / primary action buttons"),
        max_length=10,
        verbose_name=_("text color"),
    )
    css_save_button_text_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_save_button_text_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_button_font_size = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text=_("e.g. 13px · Leave blank to use the browser default (13px)."),
        verbose_name=_("font size"),
    )
    css_button_border_radius = models.CharField(
        max_length=20,
        blank=True,
        default="0.3rem",
        help_text=_("e.g. 4px · 50% · Leave blank for no rounding."),
        verbose_name=_("border radius"),
    )

    css_action_button_background_color = ColorField(
        blank=True,
        default="#888888",
        help_text=_("Background colour of capsule-shaped action buttons (History, Duplicate, etc.)"),
        max_length=10,
        verbose_name=_("background color"),
    )
    css_action_button_background_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_action_button_background_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_action_button_background_hover_color = ColorField(
        blank=True,
        default="#747474",
        help_text=_("Action button background colour on hover"),
        max_length=10,
        verbose_name=_("hover background"),
    )
    css_action_button_background_hover_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_action_button_background_hover_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_action_button_text_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Text colour on action buttons"),
        max_length=10,
        verbose_name=_("text color"),
    )
    css_action_button_text_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_action_button_text_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_delete_button_background_color = ColorField(
        blank=True,
        default="#d81a00",
        help_text=_("Background colour of Delete / danger buttons"),
        max_length=10,
        verbose_name=_("background color"),
    )
    css_delete_button_background_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_delete_button_background_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_delete_button_background_hover_color = ColorField(
        blank=True,
        default="#a31500",
        help_text=_("Delete button background colour on hover"),
        max_length=10,
        verbose_name=_("background hover color"),
    )
    css_delete_button_background_hover_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_delete_button_background_hover_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_delete_button_text_color = ColorField(
        blank=True,
        default="#FFFFFF",
        help_text=_("Text colour on Delete / danger buttons"),
        max_length=10,
        verbose_name=_("text color"),
    )
    css_delete_button_text_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_delete_button_text_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_success_color = ColorField(
        blank=True,
        default="#28A745",
        help_text=_("#28A745 — used for OK/healthy states in plugin dashboards"),
        max_length=10,
        verbose_name=_("success / OK color"),
    )
    css_success_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_success_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_warning_color = ColorField(
        blank=True,
        default="#ddab52",
        help_text=_("#ddab52 — used for paused items, warnings, and amber UI states"),
        max_length=10,
        verbose_name=_("warning / paused color"),
    )
    css_warning_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_warning_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_muted_color = ColorField(
        blank=True,
        default="#999999",
        help_text=_("#999999 — used for disabled items, secondary text, and muted UI states"),
        max_length=10,
        verbose_name=_("muted / disabled color"),
    )
    css_muted_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_muted_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_alert_color = ColorField(
        blank=True,
        default="#BA2121",
        help_text=_("#BA2121 — used for dangerous actions, error states, and alert buttons"),
        max_length=10,
        verbose_name=_("alert / danger color"),
    )
    css_alert_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_alert_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_disabled_color = ColorField(
        blank=True,
        default="#666666",
        help_text=_("#666666 — used for disabled rows and records, distinct from ordinary muted/secondary text"),
        max_length=10,
        verbose_name=_("disabled color"),
    )
    css_disabled_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_disabled_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_message_success_bg = ColorField(
        blank=True,
        default="#dff2e3",
        help_text=_("Background colour of success (green) system notifications"),
        max_length=10,
        verbose_name=_("success background"),
    )
    css_message_success_bg_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_success_bg_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_message_warning_bg = ColorField(
        blank=True,
        default="#faf3e5",
        help_text=_("Background colour of warning (amber) system notifications"),
        max_length=10,
        verbose_name=_("warning background"),
    )
    css_message_warning_bg_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_warning_bg_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_message_error_bg = ColorField(
        blank=True,
        default="#f5dede",
        help_text=_("Background colour of error (red) system notifications"),
        max_length=10,
        verbose_name=_("error background"),
    )
    css_message_error_bg_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_error_bg_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_message_info_bg = ColorField(
        blank=True,
        default="#d9f0f7",
        help_text=_("Background colour of info (cyan) system notifications"),
        max_length=10,
        verbose_name=_("info background"),
    )
    css_message_info_bg_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_info_bg_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    css_message_success_text = ColorField(
        blank=True,
        default="#1a5c2b",
        help_text=_("Text colour of success (green) system notifications"),
        max_length=10,
        verbose_name=_("success text"),
    )
    css_message_success_text_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_success_text_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_message_warning_text = ColorField(
        blank=True,
        default="#7a5000",
        help_text=_("Text colour of warning (amber) system notifications"),
        max_length=10,
        verbose_name=_("warning text"),
    )
    css_message_warning_text_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_warning_text_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_message_error_text = ColorField(
        blank=True,
        default="#6b0f0f",
        help_text=_("Text colour of error (red) system notifications"),
        max_length=10,
        verbose_name=_("error text"),
    )
    css_message_error_text_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_error_text_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    css_message_info_text = ColorField(
        blank=True,
        default="#004d66",
        help_text=_("Text colour of info (cyan) system notifications"),
        max_length=10,
        verbose_name=_("info text"),
    )
    css_message_info_text_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    css_message_info_text_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))

    related_modal_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
    )
    related_modal_background_color = ColorField(
        blank=True,
        default="#000000",
        help_text=_("Colour of the overlay behind related-object popups"),
        max_length=10,
        verbose_name=_("background color"),
    )
    related_modal_background_color_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    related_modal_background_color_dark = ColorField(blank=True, default="", max_length=10, verbose_name=_("dark"))
    related_modal_background_opacity_choices = (
        ("0.1", "10%"),
        ("0.2", "20%"),
        ("0.3", "30%"),
        ("0.4", "40%"),
        ("0.5", "50%"),
        ("0.6", "60%"),
        ("0.7", "70%"),
        ("0.8", "80%"),
        ("0.9", "90%"),
    )
    related_modal_background_opacity = models.CharField(
        max_length=5,
        choices=related_modal_background_opacity_choices,
        default="0.3",
        help_text=_("Opacity of the overlay behind related-object popups"),
        verbose_name=_("background opacity"),
    )
    related_modal_background_opacity_dark_use = models.BooleanField(default=False, verbose_name=_("dark?"))
    related_modal_background_opacity_dark = models.CharField(
        max_length=5,
        choices=related_modal_background_opacity_choices,
        default="0.3",
        blank=True,
        verbose_name=_("dark"),
    )
    related_modal_rounded_corners = models.BooleanField(
        default=True,
        verbose_name=_("rounded corners"),
    )
    related_modal_close_button_visible = models.BooleanField(
        default=True,
        verbose_name=_("close button visible"),
    )

    list_filter_highlight = models.BooleanField(
        default=True,
        verbose_name=_("highlight active"),
    )
    list_filter_dropdown = models.BooleanField(
        default=True,
        verbose_name=_("use dropdown"),
    )
    list_filter_sticky = models.BooleanField(
        default=True,
        verbose_name=_("sticky position"),
    )
    list_filter_removal_links = models.BooleanField(
        default=True,
        verbose_name=_("quick remove links for active filters at top of sidebar"),
    )

    foldable_apps = models.BooleanField(
        default=True,
        verbose_name=_("foldable apps"),
    )

    show_fieldsets_as_tabs = models.BooleanField(
        default=False,
        verbose_name=_("fieldsets as tabs"),
    )

    show_inlines_as_tabs = models.BooleanField(
        default=False,
        verbose_name=_("inlines as tabs"),
    )

    collapsible_stacked_inlines = models.BooleanField(
        default=False,
        verbose_name=_("collapsible stacked inlines"),
    )
    collapsible_stacked_inlines_collapsed = models.BooleanField(
        default=True,
        verbose_name=_("collapsible stacked inlines collapsed"),
    )
    collapsible_tabular_inlines = models.BooleanField(
        default=False,
        verbose_name=_("collapsible tabular inlines"),
    )
    collapsible_tabular_inlines_collapsed = models.BooleanField(
        default=True,
        verbose_name=_("collapsible tabular inlines collapsed"),
    )

    recent_actions_visible = models.BooleanField(
        default=True,
        verbose_name=_("visible"),
    )

    form_actions_sticky = models.BooleanField(
        default=True,
        verbose_name=_("sticky actions"),
    )
    form_submit_sticky = models.BooleanField(
        default=True,
        verbose_name=_("sticky submit"),
    )
    form_pagination_sticky = models.BooleanField(
        default=True,
        verbose_name=_("sticky pagination"),
    )

    objects = ThemeQuerySet.as_manager()

    def clean(self):
        from django.core.exceptions import ValidationError

        from .validators import (
            THEME_COLOR_FIELDS,
            THEME_DIMENSION_FIELDS,
            validate_css_dimension,
            validate_css_font_family,
            validate_theme_name,
        )

        errors = {}

        def _check(field_name, validator):
            try:
                validator(getattr(self, field_name) or "")
            except ValidationError as exc:
                errors[field_name] = exc

        for field_name in THEME_COLOR_FIELDS:
            value = (getattr(self, field_name) or "").strip()
            setattr(self, field_name, value)

        for field_name in THEME_DIMENSION_FIELDS:
            _check(field_name, validate_css_dimension)

        _check("css_body_font_family", validate_css_font_family)
        _check("name", validate_theme_name)

        if errors:
            raise ValidationError(errors)

    def set_active(self):
        self.active = True
        self.save()

    class Meta:
        app_label = "admin_interface"
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def __str__(self):
        return force_str(self.name)


@receiver(post_delete, sender=Theme)
def post_delete_handler(sender, instance, **kwargs):
    del_cached_active_theme()
    Theme.objects.get_active()
    if not getattr(instance, "_preserve_media", False):
        theme_dir = Path(settings.MEDIA_ROOT) / "admin-interface" / "themes" / instance.name
        if theme_dir.exists():
            shutil.rmtree(theme_dir)


@receiver(post_save, sender=Theme)
def post_save_handler(sender, instance, **kwargs):
    del_cached_active_theme()
    if instance.active:
        Theme.objects.exclude(pk=instance.pk).update(active=False)
    Theme.objects.get_active()


@receiver(pre_save, sender=Theme)
def pre_save_handler(sender, instance, **kwargs):
    if instance.pk is None:
        try:
            obj = Theme.objects.get(name=instance.name)
            instance.pk = obj.pk
        except Theme.DoesNotExist:
            pass
