from django.db.models.base import ModelBase
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.text import capfirst
from django.apps import apps


class AlreadyRegistered(Exception):
    pass


class BackofficeOptionException(Exception):
    pass


class BackofficeOptions:
    """
    Class options to configure the register model
    """

    list_display = ()
    list_per_page = 50
    search_fields = ()
    form_column_style = 1

    # crud_mode to select func Create, Read, Update, Delete
    # default option is `crud`, and `r` or read mode can't disable
    crud_mode = 'crud'
    icon_menu = ''

    def __init__(self, model, opts_class):
        self.model = model
        self.model_meta = model._meta
        self.opts_class = opts_class
        super().__init__()

    def __str__(self):
        return "%s.%s" % (self.model_meta.app_label, self.__class__.__name__)

    def _get_field_names(self):
        """
        To get all field names of model
        """
        return [f.name for f in self.model._meta.get_fields()]

    def _get_name_model(self):
        return capfirst(self.model._meta.verbose_name_plural)

    def _get_name_app(self):
        return capfirst(apps.get_app_config(self.model._meta.app_label).verbose_name)

    def list_view(self, request):
        """
        CreateView to show all data of model
        """
        from djbackoffice.views import ListView
        class_view = ListView
        class_view.backoffice = self.opts_class
        class_view.model = self.model
        class_view.crud_mode = self.crud_mode
        class_view.search_fields = self.search_fields
        class_view.fields = self.list_display or tuple(self._get_field_names())
        class_view.paginate_by = self.list_per_page
        class_view.search_fields = self.search_fields
        class_view.model_meta = self.model_meta
        class_view.title_page = "List %s" % self._get_name_model()
        class_view.sub_title = "On App %s" % self._get_name_app()
        return class_view.as_view()(request)

    def add_view(self, request):
        """
        CreateView to add data of model
        """
        from djbackoffice.views import CreateView
        class_view = CreateView
        class_view.backoffice = self.opts_class
        class_view.model = self.model
        class_view.model_meta = self.model_meta
        class_view.title_page = "Add %s" % self._get_name_model()
        class_view.sub_title = "On App %s" % self._get_name_app()
        class_view.template_name = self.get_form_colum_style()
        return class_view.as_view()(request)

    def edit_view(self, request, pk):
        """
        UpdateView to update data of model
        """
        from djbackoffice.views import UpdateView
        class_view = UpdateView
        class_view.backoffice = self.opts_class
        class_view.model = self.model
        class_view.model_meta = self.model_meta
        class_view.title_page = "Edit %s" % self._get_name_model()
        class_view.sub_title = "On App %s" % self._get_name_app()
        class_view.template_name = self.get_form_colum_style()
        return class_view.as_view()(request, pk=pk)

    def delete_view(self, request, pk):
        """
        DeleteView to remove data of model
        """
        from djbackoffice.views import DeleteView
        class_view = DeleteView
        class_view.model = self.model
        class_view.model_meta = self.model_meta
        return class_view.as_view()(request, pk=pk)

    def detail_view(self, request, pk):
        """
        DetailView to show all data of model
        """
        from djbackoffice.views import DetailView
        class_view = DetailView
        class_view.backoffice = self.opts_class
        class_view.model = self.model
        class_view.model_meta = self.model_meta
        class_view.sub_title = "On App %s" % self._get_name_app()
        return class_view.as_view()(request, pk=pk)

    def get_urls(self):
        """
        Generates a CRUD url from a registered model
        """
        from django.urls import path
        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            path('', self.list_view, name='%s_%s_list' % info),
            path('detail/<path:pk>/', self.detail_view, name='%s_%s_detail' % info),
        ]
        if 'c' in self.crud_mode.lower():
            print("create mode", self.model_meta)
            urlpatterns += [path('add/', self.add_view, name='%s_%s_add' % info)]
        if 'u' in self.crud_mode.lower():
            urlpatterns += [path('edit/<path:pk>/', self.edit_view, name='%s_%s_edit' % info)]
        if 'd' in self.crud_mode.lower():
            urlpatterns += [path('delete/<path:pk>/', self.delete_view, name='%s_%s_delete' % info)]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    def get_form_colum_style(self):
        """
        Returns the template according to the desired number of columns
        """
        if self.form_column_style == 1:
            return 'djbackoffice/partials/one-column-form.html'
        elif self.form_column_style == 2:
            return 'djbackoffice/partials/two-column-form.html'
        else:
            raise BackofficeOptionException("form_column_style set using 1 or 2")


class Backoffice(object):
    """
    A Backoffice object encapsulates an instance of a backoffice. Models are
    registered with the Backoffice using the register() method.
    """
    index_title = 'Backoffice'

    def __init__(self, name='djbackoffice'):
        self._registry = {}
        self.name = name

    def register(self, model_or_iterable, opts_class=None):
        """
        Registers the given model(s) with the given BackofficeOptions.
        The model(s) should be Model classes, not instances.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        opts_class = opts_class or BackofficeOptions

        for model in model_or_iterable:
            if model in self._registry:
                if model in self._registry:
                    raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            self._registry[model] = opts_class(model, self)

    def index(self, request):
        """
        Display the main backoffice index page
        """
        sidebar_menu = self.get_app_menu_register()

        context = {
            'title': self.index_title,
            'sidebar_menu': sidebar_menu,
        }

        request.current_app = self.name
        return TemplateResponse(request, 'djbackoffice/home.html', context)

    def get_urls(self):
        """
        Collect all urls of the registered models
        """
        from django.urls import path, include
        from django.contrib.admin import AdminSite

        # Admin-site views.
        admin = AdminSite()
        admin.login_template = 'djbackoffice/login.html'
        admin.logout_template = 'djbackoffice/login.html'

        urlpatterns = [
            path('', self.index, name='index'),
            path('login/', admin.login, name='login'),
            path('logout/', admin.logout, name='logout'),
        ]
        for model, backoffice_opts in self._registry.items():
            urlpatterns += [
                path('%s/%s/' % (model._meta.app_label, model._meta.model_name), include(backoffice_opts.urls)),
            ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'djbackoffice', self.name

    def get_app_menu_register(self):
        """
        Creates a menu sidebar based on the app name and registered model
        """
        app_dict = {}

        models = self._registry
        for model, opts in models.items():
            app_label = model._meta.app_label

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'admin_url': reverse('djbackoffice:%s_%s_list' % info),
                'icon_menu': opts.icon_menu
            }

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'models': [model_dict],
                }

        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list


backoffice = Backoffice()
