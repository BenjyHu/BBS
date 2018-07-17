"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    path('code/', views.code, name='code'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('up_down/', views.up_down, name='up_down'),
    path('comment/', views.comment, name='comment'),
    path('backend/', views.backend, name='backend'),
    path('add_article/', views.add_article, name='add_article'),
    path('upload/', views.upload, name='upload'),
    path('delete_article/', views.delete_article, name='delete_article'),
    re_path('edit_article/(?P<pk>\d+)', views.edit_article, name='edit_article'),
    re_path(r'(?P<name>\w+)/(?P<subName>category|tag|archive)/(?P<arg>.+)', views.my_site),
    re_path(r'^(?P<name>\w+)/$', views.my_site, name='my_site'),
    re_path(r'^(?P<name>\w+)/article/(?P<article_id>\d+)/$', views.article_info, name='article_info'),

]
