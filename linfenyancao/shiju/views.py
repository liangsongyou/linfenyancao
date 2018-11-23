from django.shortcuts import render, get_object_or_404

from .models import  Artical, Lanmu


# 市局
def shiju(request):
    return render(request, 'shiju/index.html',{})

# 临烟动态
def dongtai(request,name=None):
    _lanmu = get_object_or_404(Lanmu, name=name)
    articals = Artical.objects.filter(lanmu__name=name)
    context = {
        'articals':articals,
        'lanmu':_lanmu
    }
    return render(request, 'shiju/dongtai.html',context)

# 文章
def artical(request, pk=None):
    item = get_object_or_404(Artical, pk=pk)
    context = {
        'item':item
    }
    return render(request, 'shiju/artical.html', context)

# 领导
def lingdao(request):
    return render(request, 'shiju/lingdao.html', {})

# dwebcms登录
# def cms_login(request):
#     return render(request, 'dwebcms/login.html')

# dwebcms管理首页
def cms_index(request):
    return render(request, 'dwebcms/index.html')

# dwebcms新建栏目
def cms_newLanmu(request):
    return render(request, 'dwebcms/newLanmu.html')

# dwebcms栏目列表
def cms_listLanmu(request):
    return render(request, 'dwebcms/listLanmu.html')
