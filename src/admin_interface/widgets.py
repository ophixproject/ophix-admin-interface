from django import forms


class Select2Widget(forms.Select):
    """
    A plain choice <select> that opt-ins to Select2 initialisation via select2-init.js.
    Use via formfield_for_choice_field in ModelAdmin subclasses.
    """
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        css_class = attrs.get("class", "")
        if "vSelect2" not in css_class:
            attrs["class"] = (css_class + " vSelect2").strip()
        return attrs
