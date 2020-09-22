from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Cooli Express API Endpoints",
        default_version="v1",
        description="API endpoints for Cooli Express backend application",
        terms_of_service="",
        contact=openapi.Contact(email="farhadurfahim@gmail.com"),
        license=openapi.License(name="Closed Source License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

doc_patterns = ([
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
], "docs")


api_patterns = ([
    path("docs/", include(doc_patterns, namespace="docs")),
    path("users/", include("cooli_express.users.api.urls", namespace="users")),
    path("customers/", include("cooli_express.customers.api.urls", namespace="customers")),
    path("orders/", include("cooli_express.orders.urls", namespace="orders")),
], "api")

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),
    path('', lambda request: redirect('admin/'), name="home"),
    path('about/', RedirectView.as_view(url='/')),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    path(
        f"api/{settings.API_VERSION}/",
        include(api_patterns, namespace=settings.API_VERSION_NAMESPACE)
    ),

    # User management
    path("users/", include("cooli_express.users.urls", namespace="users_module")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

from .super_admin_site import  super_site
urlpatterns += [
    path('super-admin/', super_site.urls),
]
