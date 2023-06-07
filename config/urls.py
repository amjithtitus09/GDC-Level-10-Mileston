from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("task_manager.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]


from rest_framework.routers import DefaultRouter, SimpleRouter

from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LogoutView

from task_manager.tasks.views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    session_storage_view,
    UserSignupView,
    UserLoginView,
    CompletedTaskListView,
    TaskDetailView,
    TaskCompleteView,
    UserUpdateView,
)

from task_manager.tasks.apiviews import TaskViewSet, HistoryViewSet

from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from task_manager.users.api.views import UserViewSet

from task_manager.tasks.apiviews import TaskViewSet, HistoryViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("api/task", TaskViewSet)

tasks_router = NestedSimpleRouter(router, "api/task", lookup="task")
tasks_router.register(r"history", HistoryViewSet, basename="task-history")

app_name = "api"
urlpatterns += (
    [
        path("sessionviews/", session_storage_view),
        path("user/signup", UserSignupView.as_view()),
        path("user/login", UserLoginView.as_view()),
        path("user/logout", LogoutView.as_view()),
        path("tasks/", TaskListView.as_view()),
        path("create-task/", TaskCreateView.as_view()),
        path("update-task/<pk>", TaskUpdateView.as_view()),
        path("update-user/<pk>", UserUpdateView.as_view()),
        path("delete-task/<pk>/", TaskDeleteView.as_view()),
        path("view-task/<pk>/", TaskDetailView.as_view()),
        path("complete_task/<pk>/", TaskCompleteView.as_view()),
        path("completed_tasks/", CompletedTaskListView.as_view()),
    ]
    + router.urls
    + tasks_router.urls
)


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
