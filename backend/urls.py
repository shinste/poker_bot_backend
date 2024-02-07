from django.urls import path
from .views.initialize import Initialize
from django.contrib import admin

urlpatterns = [
    path('initiate/', Initialize.as_view(), name="initialize game"),
    path('', admin.site.urls, name="homepage"),
]