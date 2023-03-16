"""pcb_detection URL Configuration

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
from django.contrib import admin
from django.urls import path
from detection import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload),
    path('check/',views.check),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    path('show_book/', views.show_book_func,name='show_view'),
    path('show_check/', views.show_check_func,name='show_check'),
    path('show_defect/',views.show_defect,name='show_defect')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)