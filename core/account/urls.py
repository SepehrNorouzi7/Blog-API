from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('api/v1/',include('account.api.v1.urls')),
]