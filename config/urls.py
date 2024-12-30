from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        # название нашей документации
        title="Retail chain API",
        # версия документации
        default_version="v1.0.0",
        # описание нашей документации
        description="Retail chain API description",
        terms_of_service="https://localhost/policies/terms/",
        contact=openapi.Contact(email="alina_nemo@mail.ru"),
        license=openapi.License(name="Retail chain API License"),
    ),
    public=True,
    # в разрешениях можем сделать доступ только авторизованным пользователям.
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("retail_chain.urls", namespace="retail_chain")),
    path("users/", include("users.urls", namespace="users")),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
