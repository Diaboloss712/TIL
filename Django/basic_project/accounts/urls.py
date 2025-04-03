from django.urls import path, include
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete/', views.delete, name='index'),
    path('update/', views.update, name='update'),
]