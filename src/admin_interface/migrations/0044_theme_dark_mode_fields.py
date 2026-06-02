import colorfield.fields
from django.db import migrations, models
from django.utils.translation import gettext_lazy as _

_DARK_COLOR = dict(blank=True, default="", max_length=10, verbose_name=_("dark"))
_DARK_USE = dict(default=False, verbose_name=_("dark?"))

PAIRS = [
    "title_color",
    "logo_color",
    "env_color",
    "css_header_background_color",
    "css_header_text_color",
    "css_header_link_color",
    "css_header_link_hover_color",
    "css_module_background_color",
    "css_module_background_selected_color",
    "css_module_text_color",
    "css_module_link_color",
    "css_module_link_selected_color",
    "css_module_link_hover_color",
    "css_generic_link_color",
    "css_generic_link_hover_color",
    "css_generic_link_active_color",
    "css_save_button_background_color",
    "css_save_button_background_hover_color",
    "css_save_button_text_color",
    "css_delete_button_background_color",
    "css_delete_button_background_hover_color",
    "css_delete_button_text_color",
    "css_success_color",
    "css_warning_color",
    "css_muted_color",
    "css_alert_color",
    "related_modal_background_color",
]


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0043_theme_helptext"),
    ]

    operations = [
        op
        for base in PAIRS
        for op in (
            migrations.AddField(
                model_name="theme",
                name=f"{base}_dark_use",
                field=models.BooleanField(**_DARK_USE),
            ),
            migrations.AddField(
                model_name="theme",
                name=f"{base}_dark",
                field=colorfield.fields.ColorField(**_DARK_COLOR),
            ),
        )
    ]
