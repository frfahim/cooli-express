from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = "users"


token_patterns = (
    [
        path("refresh/", TokenRefreshView.as_view(), name="refresh"),
        path("verify/", TokenVerifyView.as_view(), name="verify"),
    ],
    "token",
)

auth_urls = (
    [
        path('', include('dj_rest_auth.urls')),
        path('registration/', include('dj_rest_auth.registration.urls'))
    ],
    "auth",
)

urlpatterns = [
    path("token/", include(token_patterns, namespace="token")),
    path("auth/", include(auth_urls, namespace="auth")),
]
