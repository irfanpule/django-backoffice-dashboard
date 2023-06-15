# Django Backoffice Dashboard

Django Backoffice is an application Django to easier create backoffice dashboard integrated for your project.
![img](https://github.com/irfanpule/django-backoffice-dashboard/raw/main/docs/screnshots/ss1.png?raw=true)
 
## Installation
- Install django-backoffice using:
    ```
    pip install django-backoffice-dashboard-alpha
    ```

- Add `djbackoffice` to your `INSTALLED_APPS` setting like this
    ```
    INSTALLED_APPS = [
        ...
        'djbackoffice',
    ]
    ```
- Run `python manage.py collectstatic` to collect file static djbackoffice into project.
- Include url `djbackoffice` in your root url
    ```
    from djbackoffice.core import backoffice
    ....

    urlpatterns = [
        path('admin/', admin.site.urls),
        .....
        path('backoffice/', backoffice.urls),
    ]
    ```
  
- Access `http://127.0.0.1:8000/backoffice/login/` to enter backoffice page.

## How to Use
- create file `backoffice.py` on your app
- Then write
#### Simple register
```python
from djbackoffice.core import backoffice
from author.models import Author

backoffice.register(Author)
```
#### Advanced register
```python
from djbackoffice.core import backoffice, BackofficeOptions
from djbackoffice.decorators import register
from author.models import Author


@register(Author)
class AuthorOption(BackofficeOptions):
    # To select the fields that will appear in the index view 
    list_display = ('name', 'email', 'address', 'phone_number')
    
    # To select the field to be the search key
    search_fields = ('name', 'email')
    
    # To select a form layout
    form_column_style = 2
    
    # To select CRUD mode. The default Read mode cannot be disabled
    crud_mode = 'cru'
    
    # To set how much data appears in the index view
    list_per_page = 50
    
    # To set the icon that appears on the menu
    # icon using https://icons.getbootstrap.com
    icon_menu = "bi-door-open-fill"
```

## Thanks!
- https://github.com/zuramai/mazer: Mazer Dashboard Template

## For Contributor
- clone project
- symlink app to `demo`
  ```bash
  ln -s [path_project_djbackoffice] [path_demo_djbackoffice]
  ```
- create `env` development
- active `env`
- enter directory `demo`
- now, you can access all command `manage.py`

## TODO
- [ ] Permission Access
- [ ] Custom Dashboard
- [ ] Organize Sidebar Menu
- [ ] Advance Filter
