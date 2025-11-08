"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from core import views as v

urlpatterns = [
    path("admin/", admin.site.urls),

    # Páginas
    path("", v.login_page, name="login_page"),                 # <<— raíz muestra tu login
    path("login/", v.login_page),                              # alias opcional
    path("dashboard/", v.dashboard_empleado, name="dash_empleado"),
    path("dashboard-admin/", v.dashboard_admin, name="dash_admin"),

    # API
    path("api/login/", v.login_json, name="login_json"),
    path("api/logout/", v.logout_view, name="logout"),
]



