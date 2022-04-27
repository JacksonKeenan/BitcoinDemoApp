from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('public-wallets/', index),
    path('public-wallets/<str:address>', index),
]
