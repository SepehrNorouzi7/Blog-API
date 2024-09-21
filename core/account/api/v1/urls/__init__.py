from django.urls import path, include

urlpatterns = [
    path("", include("account.api.v1.urls.accounts")),
    path("profile/", include("account.api.v1.urls.profiles")),
]