import colorfield.fields
from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):
    """
    State-only migration: update help_text on all color fields from hex placeholder
    values to descriptive strings. No database changes.
    """

    dependencies = [
        ("admin_interface", "0042_theme_new_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theme",
            name="title_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#F5DD5D",
                help_text=_("Colour of the title text in the header bar"),
                max_length=10,
                verbose_name=_("color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="logo_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text=_("Tint applied to the logo SVG; white shows the logo unchanged"),
                max_length=10,
                verbose_name=_("color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_header_background_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#0C4B33",
                help_text=_("Background colour of the top header bar"),
                max_length=10,
                verbose_name=_("background color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_header_text_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#44B78B",
                help_text=_("Colour of plain text in the header bar"),
                max_length=10,
                verbose_name=_("text color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_header_link_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text=_("Colour of navigation links in the header bar"),
                max_length=10,
                verbose_name=_("link color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_header_link_hover_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#C9F0DD",
                help_text=_("Header link colour on hover"),
                max_length=10,
                verbose_name=_("link hover color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_module_background_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#44B78B",
                help_text=_("Background colour of section header bars (module titles)"),
                max_length=10,
                verbose_name=_("background color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_module_background_selected_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFCC",
                help_text=_("Background colour of selected / highlighted rows"),
                max_length=10,
                verbose_name=_("background selected color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_module_text_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text=_("Text colour inside section header bars"),
                max_length=10,
                verbose_name=_("text color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_module_link_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text=_("Link colour inside section header bars"),
                max_length=10,
                verbose_name=_("link color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_module_link_selected_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text=_("Link colour for selected items inside section header bars"),
                max_length=10,
                verbose_name=_("link selected color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_module_link_hover_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#C9F0DD",
                help_text=_("Link colour on hover inside section header bars"),
                max_length=10,
                verbose_name=_("link hover color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_generic_link_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#0C3C26",
                help_text=_("Default link colour in page content"),
                max_length=10,
                verbose_name=_("link color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_generic_link_hover_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#156641",
                help_text=_("Page content link colour on hover"),
                max_length=10,
                verbose_name=_("link hover color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_generic_link_active_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#29B864",
                help_text=_("Page content link colour when active / pressed"),
                max_length=10,
                verbose_name=_("link active color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_save_button_background_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#0C4B33",
                help_text=_("Background colour of Save / primary action buttons"),
                max_length=10,
                verbose_name=_("background color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_save_button_background_hover_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#0C3C26",
                help_text=_("Save button background colour on hover"),
                max_length=10,
                verbose_name=_("background hover color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_save_button_text_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text=_("Text colour on Save / primary action buttons"),
                max_length=10,
                verbose_name=_("text color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_delete_button_background_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#BA2121",
                help_text=_("Background colour of Delete / danger buttons"),
                max_length=10,
                verbose_name=_("background color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_delete_button_background_hover_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#A41515",
                help_text=_("Delete button background colour on hover"),
                max_length=10,
                verbose_name=_("background hover color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_delete_button_text_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text=_("Text colour on Delete / danger buttons"),
                max_length=10,
                verbose_name=_("text color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="related_modal_background_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#000000",
                help_text=_("Colour of the overlay behind related-object popups"),
                max_length=10,
                verbose_name=_("background color"),
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="related_modal_background_opacity",
            field=models.CharField(
                choices=[
                    ("0.1", "10%"),
                    ("0.2", "20%"),
                    ("0.3", "30%"),
                    ("0.4", "40%"),
                    ("0.5", "50%"),
                    ("0.6", "60%"),
                    ("0.7", "70%"),
                    ("0.8", "80%"),
                    ("0.9", "90%"),
                ],
                default="0.3",
                help_text=_("Opacity of the overlay behind related-object popups"),
                max_length=5,
                verbose_name=_("background opacity"),
            ),
        ),
    ]
