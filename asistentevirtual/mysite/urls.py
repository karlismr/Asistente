"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from chat.views import ejecutar_revision_cron


urlpatterns = [
    path('admin/', admin.site.urls),
     path('chat/', include('chat.urls')),
     path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
      path('', RedirectView.as_view(url='/chat/', permanent=False)),
      path('ejecutar-cron-secreto/', ejecutar_revision_cron, name='cron_notificaciones'),

      path('manifest.json', TemplateView.as_view(
        template_name='manifest.json', 
        content_type='application/json'
    )),
    path('serviceworker.js', TemplateView.as_view(
        template_name='serviceworker.js', 
        content_type='application/javascript'
    )),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)