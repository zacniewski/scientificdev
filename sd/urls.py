"""sd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings as my_settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ambro-met/', include('ambro.urls', namespace='ambro')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', include('frontend.urls', namespace='frontend')),
    path('newsletter/', include('newsletter.urls', namespace='newsletter')),
    path('tinymce/', include('tinymce.urls')),
]

handler404 = 'frontend.views.handler404'
handler500 = 'frontend.views.handler500'

if my_settings.DEBUG:
    urlpatterns += static(my_settings.MEDIA_URL, document_root=my_settings.MEDIA_ROOT)
