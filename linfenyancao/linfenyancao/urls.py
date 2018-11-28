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
    # 文章列表
    path('list/<int:pk>/', views.artical_list, name='articallist'),
    # 文章细节页面
    path('artical/<int:pk>/',views.artical, name='artical'),

    # 县局页面
    path('xianju/<int:pk>/',views.xianju, name="xianju"),
    path('keshi/<int:pk>/',views.keshi,name='keshi'),
    path('keshi/teshu/',views.teshu_keshi,name='teshukeshi'),


    # dwebcms登录
    # path('cms/login',views.cms_login, name='登录'),
    # dwebcms管理首页
    path('cms/index/',views.cms_index, name='管理首页'),
    # dwebcms新建栏目
    path('cms/newlanmu',views.cms_newLanmu, name='newLanmu'),
    # dwebcms栏目列表
    path('cms/listlanmu',views.cms_listLanmu, name='listLanmu'),
    # dwebcms删除子栏目
    path('cms/sublanmu/<int:pk>/delete/',views.cms_deleteSubLanmu, name="删除子栏目"),
    path('cms/sublanmu/<int:pk>/zhiding/',views.cms_zhidingSubLanmu, name="zhiding"),

    # dwebcms文章发布
    path('cms/wztijiao/<str:jigou_name>/',views.cms_wzTijiao, name="wzTijiao"),
    # dwebcms文章列表
    path('cms/wzlist/',views.cms_wzList, name="wzList"),
    # dwebcms文章删除
    path('cms/wzdelete/<int:pk>/',views.cms_wzDelete, name="wzDelete"),

    # dwebcms文章还原
    path('cms/wzhuanyuan/<int:pk>/',views.cms_wzHuanyuan, name="wzHuanyuan"),

    # dwebcms文章修改
    path('cms/wzxiugai/<int:pk>/',views.cms_wzXiugai, name="wzXiugai"),
    # dwebcms文章回收
    path('cms/wzhuishou/',views.cms_wzHuishou, name="wzHuishou"),

    # dwebcms文章彻底删除
    path('cms/wzhuishou/<int:pk>/',views.cms_wzDelete_cd, name='wzDelete_cd'),

    # accounts
    path('accounts/', include('django.contrib.auth.urls')),

    # 默认
    path('', views.shiju, ),
    # 富文本
    path('ueditor/', include('DjangoUeditor.urls' ) ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
