"""gatewaysystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import path, include,re_path
from django.contrib import admin
from app import views, urls as app_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.loginview, name='loginview'),
    path('accounts/login/renew/', views.loginrenew, name='loginrenew'),
    path('changepwd/', views.changepwd, name='changepwd'),
    path('auth/', views.auth, name='auth'),
    path('search_n/', views.search_n, name='search_n'),

    #path('auth/callback/', views.oauthcallback, name='oauthcallback'),
    path('logoff/', views.logoff, name='logoff'),
    path('aninewreg/', views.aninewreg, name='aninewreg'),
    path('topupreport/', views.topupreport, name='topupreport'),
    path('topupstatus/', views.topupstatus, name='topupstatus'),
    path('view015number/', views.view015number, name='view015number'),
    path('available015number/', views.available015number, name='available015number'),
    path('createlogin/', views.createlogin, name='createlogin'),
    # path('createstate/', views.createstate, name='createstate'),
    path('app/', include(app_urls)),
    path('admin/', admin.site.urls),
    path('callback/', views.oauthcallback, name='oauthcallback'),
    path('createstate/', views.createstate, name='createstate'),
    path('createstate_/', views.createstate_, name='createstate_'),
    path('assignnumberstate_/', views.assignnumberstate_, name='assignnumberstate_'),
    path('assign015number/', views.assign015number, name='assign015number'),

    path('assign015number_update/', views.assign015number_update, name='assign015number_update'),
    path('view015numberbatchid/', views.view015numberbatchid, name='view015numberbatchid'),
    path('reserve015number/', views.reserve015number, name='reserve015number'),


    path('reserve015number_update/', views.reserve015number_update, name='reserve015number_update'),
    path('createmanager/', views.createmanager, name='createmanager'),
    path('createmanager_/', views.createmanager_, name='createmanager_'),












]
