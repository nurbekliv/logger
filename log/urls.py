from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),

    path("", views.HomeView.as_view(), name="home"),
    path("codes/<int:pk>/download/", views.download_code, name="code_download"),

    # Screenshot upload (web form)
    path("screenshots/upload/", views.ScreenshotUploadView.as_view(), name="screenshot_upload"),

    # Screenshot upload (API - device yuboradi)
    path("api/screenshots/upload/", views.api_screenshot_upload, name="api_screenshot_upload"),
]
