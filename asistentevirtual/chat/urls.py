from django.urls import path
from .views import chat_view, configurar_asistente
from django.contrib.auth import views as auth_views
from . import views 
from django.contrib import admin

urlpatterns = [
    path('', chat_view, name='chat_view'),
    path('admin/', admin.site.urls),
      path('configurar/', configurar_asistente, name='configurar_asistente'),
      path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]