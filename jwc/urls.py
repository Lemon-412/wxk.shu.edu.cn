"""jwc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from myWEB import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('calculate/', views.calculate),
    path('calculate-history/', views.calculate_history),

    path('login', views.login),
    path('login_view/', views.login_view),  # 填写完信息后提交登陆验证
    path('logout_view/', views.logout_view),  # 退出登陆

    path('index', views.index),
]
