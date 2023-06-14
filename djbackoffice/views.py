import sweetify
from django.forms.models import model_to_dict
from django.views.generic.detail import BaseDetailView, DetailView
from django.views.generic.edit import DeletionMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from djbackoffice.mixin import BackofficeContextMixin, BackOfficeFilterMixin
from djbackoffice.utils import Logger
from django_tables2 import SingleTableMixin
from django_tables2 import tables
from djbackoffice.tables import SimpleTable
from djbackoffice.settings import DJANGO_TABLES2_TEMPLATE


class ListView(BackofficeContextMixin, BackOfficeFilterMixin, SingleTableMixin, ListView):
    table_class = SimpleTable
    model_meta = None
    template_name = "djlakang/general_list.html"
    fields = ()
    crud_mode = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info = self.model_meta.app_label, self.model_meta.model_name
        if "c" in self.crud_mode.lower():
            context["add_url"] = "djlakang:%s_%s_add" % info
        else:
            context["add_url"] = None

        if "u" in self.crud_mode.lower():
            context["edit_url"] = "djlakang:%s_%s_edit" % info
        else:
            context["edit_url"] = None

        if "d" in self.crud_mode.lower():
            context["delete_url"] = "djlakang:%s_%s_delete" % info
        else:
            context["delete_url"] = None

        context["detail_url"] = "djlakang:%s_%s_detail" % info
        context["table_template"] = DJANGO_TABLES2_TEMPLATE
        return context

    def get_table_class(self):
        """
        override func from SingleTableMixin
        """
        fields = self.fields + ("actions",)
        return tables.table_factory(self.model, table=self.table_class, fields=fields)


class CreateView(BackofficeContextMixin, CreateView):
    model_meta = None
    fields = '__all__'
    form_colum_style = 1

    def form_valid(self, form):
        self.object = form.save()
        log = Logger()
        log.addition(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        sweetify.toast(self.request, "Success add %s" % self.model_meta.model_name, timer=5000)
        info = self.model_meta.app_label, self.model_meta.model_name
        pattern = 'djlakang:%s_%s_list' % info
        return reverse_lazy(pattern)


class UpdateView(BackofficeContextMixin, UpdateView):
    model_meta = None
    fields = '__all__'
    form_colum_style = 1

    def form_valid(self, form):
        self.object = form.save()
        log = Logger()
        log.change(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        sweetify.toast(self.request, "Success edit %s" % self.model_meta.model_name, timer=5000)
        info = self.model_meta.app_label, self.model_meta.model_name
        pattern = 'djlakang:%s_%s_list' % info
        return reverse_lazy(pattern)


class DeleteView(DeletionMixin, BaseDetailView):
    model_meta = None

    def delete(self, request, *args, **kwargs):
        log = Logger()
        obj = self.get_object()
        deletion = super().delete(request, *args, **kwargs)
        log.deletion(request, obj)
        return deletion

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        sweetify.toast(self.request, "Success delete %s" % self.model_meta.model_name, timer=5000)
        info = self.model_meta.app_label, self.model_meta.model_name
        pattern = 'djlakang:%s_%s_list' % info
        return reverse_lazy(pattern)


class DetailView(BackofficeContextMixin, DetailView):
    template_name = "djlakang/general_detail.html"

    def get_title_page(self):
        obj = self.get_object()
        return f"Detail data {obj.id}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["object_dict"] = model_to_dict(obj)
        return context
