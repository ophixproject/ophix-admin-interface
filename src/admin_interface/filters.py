"""
Mutually-narrowing admin list filters.

A filter built with `narrowing_filter()` computes its own option list from
the queryset scoped by whichever *other* fields in the same declared group
are currently active elsewhere on the same changelist -- never by its own
current value. That means a value already selected through one of these
filters can never become invalid purely because another filter in the
group also narrowed: each filter's choices are computed excluding itself,
so a value chosen via one narrowed list is always still present once the
group's other fields recompute around it.

Usage, in any domain's admin.py::

    from admin_interface.filters import narrowing_filter

    _my_group = narrowing_filter("target_name", "record", "reason", "actor")

    class MyAdmin(admin.ModelAdmin):
        list_filter = (
            ("target_name", _my_group),
            ("record", _my_group),
            ("reason", _my_group),
            ("actor", _my_group),
        )

Every field in the group must be given the SAME returned class (or
independently-built classes sharing the identical `fields` tuple) -- that
identical tuple is what lets each one read the others' currently-active
values. This is opt-in per admin, by design -- nothing changes on a
changelist until its own admin.py is updated to use this.

Scope: this only covers plain CharField/TextField-style filters (Django's
default `AllValuesFieldListFilter`), and only simple, same-model fields --
not `__`-lookup paths into a related model. FK-based filters
(`RelatedFieldListFilter`) are a structurally different class with their
own choice-computation logic and are not yet supported here. A sibling
factory (e.g. `narrowing_related_filter`) can be added later, reusing
`NarrowingFilterMixin` below, without reworking this one.
"""

from django.contrib import admin


class NarrowingFilterMixin:
    """
    Shared logic: scope a queryset by every OTHER currently-active field
    named in `narrowing_fields`, never by this field's own value. Reusable
    by any future filter base class, not just AllValuesFieldListFilter.
    """

    narrowing_fields = ()

    def _narrowed_queryset(self, base_queryset, request, field_path):
        queryset = base_queryset
        for other_field in self.narrowing_fields:
            if other_field == field_path:
                continue
            value = request.GET.get(other_field)
            if value:
                queryset = queryset.filter(**{other_field: value})
        return queryset


class _NarrowingAllValuesFieldListFilter(NarrowingFilterMixin, admin.AllValuesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        # Replicates AllValuesFieldListFilter.__init__ (Django's own
        # django/contrib/admin/filters.py) except for the queryset
        # lookup_choices is built from: it's additionally scoped by this
        # group's other active fields before .distinct(). Deliberately
        # skips the original's relation-path handling (reverse_field_path/
        # parent_model) -- this factory is for simple, same-model fields
        # only, which is the only case `model_admin.get_queryset(request)`
        # needs here.
        self.lookup_kwarg = field_path
        self.lookup_kwarg_isnull = "%s__isnull" % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val_isnull = params.get(self.lookup_kwarg_isnull)
        self.empty_value_display = model_admin.get_empty_value_display()
        queryset = self._narrowed_queryset(
            model_admin.get_queryset(request), request, field_path
        )
        self.lookup_choices = (
            queryset.distinct().order_by(field.name).values_list(field.name, flat=True)
        )
        # Skip AllValuesFieldListFilter's own __init__ entirely (it would
        # immediately overwrite lookup_choices with the unfiltered
        # version) -- go straight to the real FieldListFilter base, which
        # is what actually registers this filter's active parameter with
        # Django (needed for correct "remove this filter" link behavior).
        super(admin.AllValuesFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )


def narrowing_filter(*fields):
    """
    Returns a filter class scoped to `fields` (field names as they'd
    appear in `list_filter`). Use the SAME returned class for every field
    named in the group when building `list_filter`.
    """
    return type(
        "NarrowingFilter_%s" % "_".join(fields),
        (_NarrowingAllValuesFieldListFilter,),
        {"narrowing_fields": tuple(fields)},
    )
