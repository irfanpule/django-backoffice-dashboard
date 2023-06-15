# Django Backoffice

Django Backoffice is an application Django to easier create backoffice dashboard integrated for your project.

 
## Installation
- Install django-backoffice using:
    ```
    pip install django-backoffice
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
    list_display = ('name', 'email', 'address', 'phone_number')
    search_fields = ('name', 'email')
    form_column_style = 2
    crud_mode = 'cru'
    list_per_page = 50
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
- [ ] Custom Menu Sidebar
