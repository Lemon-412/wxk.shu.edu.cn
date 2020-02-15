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
    path('', views.home),  # 首页
    path('admin/', admin.site.urls),  # admin

    path('calculate/', views.calculate),  # 计算器界面
    path('calculate-history/', views.calculate_history),  # 计算历史

    path('login_view/', views.login_view),  # 填写完信息后提交登陆验证
    path('logout_view/', views.logout_view),  # 退出登陆

    path('index', views.index),  # 教务系统首页

    path('index/xk/', views.xk),  # 学生选课
    path('index/tk/', views.tk),  # 学生退课
    path('index/cjcx/', views.cjcx),  # 学生成绩查询
    path('index/kccx/', views.kccx),  # 学生课程查询

    path('index/kk/', views.kk),  # 教师开课
    path('index/qxkk/', views.qxkk),  # 教师取消开课
    path('index/fbcj/', views.fbcj),  # 教师发布成绩
]
