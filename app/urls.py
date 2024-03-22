from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catalog", views.catalog, name="catalog"),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('checkout/', views.checkout_view, name='checkout'),
    path('checked-out-books/', views.checked_out_books_view, name='checked_out_books'),
    path('checkin/', views.checkin_view, name='checkin'),
    path('accounts/create-account', views.create_account, name ='create_account'),
]
