from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catalog", views.catalog, name="catalog"),
    path('accounts/', include('django.contrib.auth.urls')),
]
