from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingredients, name='stock'),
    path('add/', views.add_ingredient, name='add'),
    path('add_buy/', views.add_buy, name='add-buy'),
    path('to_buy/', views.buy_list,name='buy'),
    path('register/',views.register, name='register'),
    path('login/',views.login_page, name='login'),
    path('logout/',views.logout_page, name='logout')
]