from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin import AdminSite
from django.apps import apps


class SuperAdminSite(AdminSite):
    site_header = "Super Admin"
    site_title = "Super Admin Portal"
    index_title = "Welcome to Super Admin Portal"

super_site = SuperAdminSite(name='super_admin')


app_models = apps.get_models()
for model in app_models:
    try:
        super_site.register(model)
    except AlreadyRegistered:
        pass
