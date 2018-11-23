from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shiju import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 市局
    path('shiju/', views.shiju, name='shiju'),
    # 领导
    path('lingdao/',views.lingdao, name='领导班子'),
    # 领导讲话
    path('<str:name>/', views.dongtai, name='临烟动态'),
    # 文章细节页面
    path('artical/<int:pk>/',views.artical, name='文章'),

    # dwebcms登录
    # path('cms/login',views.cms_login, name='登录'),
    # dwebcms管理首页
    path('cms/index/',views.cms_index, name='管理首页'),
    # dwebcms新建栏目
    path('cms/newlanmu',views.cms_newLanmu, name='newLanmu'),
    # dwebcms栏目列表
    path('cms/listlanmu',views.cms_listLanmu, name='listLanmu'),

    # accounts
    path('cms/', include('django.contrib.auth.urls')),

    # 默认
    path('', views.shiju, ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
