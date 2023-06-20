from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('token/', views.token, name='token'),
    path('product/', views.product, name='product'),

]