from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from . import views


schema_view = get_schema_view(
    openapi.Info(
        title="Warehouse API",
        default_version="v1",
        description="API books from warehouse",
    ),
    #  url=settings.SWAGGER_SETTINGS["DEFAULT_API_URL"],
    public=True,
    permission_classes=(permissions.AllowAny, ),
)


# Swagger patterns
urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]


router = DefaultRouter()
router.register(r'order', views.OrderViewSet)
router.register(r'author', views.AuthorViewSet)
router.register(r'publishing-house', views.PublishingHouseViewSet)
router.register(r'genre', views.GenreViewSet)
router.register(r'book', views.BookViewSet)
router.register(r'book-instance', views.BookInstanceViewSet)


urlpatterns += [
    path('', include(router.urls)),
    path('sync-books/', views.BookInstanceSyncList.as_view()),
]
