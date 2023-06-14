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
- Run `python manage.py collectstatic` to collect file static djf_office into project.
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



### Thanks!


### For Contributor
- clone project
- symlink app to `demo`
  ```bash
  ln -s [path_project_djf_office] [path_demo_djf_office]
  ```
- create `env` development
- active `env`
- enter directory `demo`
- now, you can access all command `manage.py`
