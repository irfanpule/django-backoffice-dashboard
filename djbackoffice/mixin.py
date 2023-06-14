from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.utils.text import unescape_string_literal, smart_split
from django.views.generic.base import ContextMixin
from djbackoffice.core import BackofficeOptions


class BackofficeContextMixin(ContextMixin):
    title_page = ''
    sub_title = ''
    btn_submit_name = ''
    backoffice: BackofficeOptions
    crud_mode = ''

    def get_title_page(self):
        return self.title_page

    def get_sub_title_page(self):
        return self.sub_title

    def get_btn_submit_name(self):
        return self.btn_submit_name

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.get_title_page()
        kwargs['title_page'] = self.get_title_page()
        kwargs['sub_title_page'] = self.get_sub_title_page()
        kwargs['btn_submit_name'] = self.get_btn_submit_name()
        kwargs['sidebar_menu'] = self.get_sidebar_menu()
        return super().get_context_data(**kwargs)

    def get_sidebar_menu(self):
        sidebar_menu = self.backoffice.get_app_menu_register()
        return sidebar_menu


class BackOfficeFilterMixin:
    search_fields = ()
    term = ''

    def get_queryset(self):
        """Return queryset. Overriding from ListView"""
        queryset = super().get_queryset()
        if self.search_fields:
            self.term = self.request.GET.get('term', '')
            qs, search_use_distinct = self.get_search_results(self.model.objects.all(), self.term)
            if search_use_distinct:
                qs = qs.distinct()
            return qs
        else:
            return queryset

    def get_search_fields(self):
        """
        Return a sequence containing the fields to be searched whenever
        somebody submits a search query.
        """
        return self.search_fields

    def get_search_results(self, queryset, search_term):
        """
        This function inspiration from django.contrib.admin.ModelAdmin

        Return a tuple containing a queryset to implement the search
        and a boolean indicating if the results may contain duplicates.
        """
        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith("^"):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith("="):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith("@"):
                return "%s__search" % field_name[1:]
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == "pk":
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, "get_path_info"):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        may_have_duplicates = False
        search_fields = self.get_search_fields()
        if search_fields and search_term:
            orm_lookups = [
                construct_search(str(search_field)) for search_field in search_fields
            ]
            for bit in smart_split(search_term):
                if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                    bit = unescape_string_literal(bit)
                or_queries = models.Q(
                    *((orm_lookup, bit) for orm_lookup in orm_lookups),
                    _connector=models.Q.OR,
                )
                queryset = queryset.filter(or_queries)
            # TODO: temporary comment
            # hardcode may_have_duplicate set False
            # may_have_duplicates |= any(
            #     lookup_spawns_duplicates(self.backoffice, search_spec)
            #     for search_spec in orm_lookups
            # )
            may_have_duplicates = False
        return queryset, may_have_duplicates

    def get_context_data(self, **kwargs):
        kwargs['use_search_form'] = True if self.get_search_fields() else False
        kwargs['search_term'] = self.term
        return super().get_context_data(**kwargs)
