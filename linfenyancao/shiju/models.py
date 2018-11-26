from django.db import models
from django.urls import reverse
from django.shortcuts import  get_object_or_404, redirect

from DjangoUeditor.models import UEditorField

# Create your models here.
class Jigou(models.Model):
    name = models.CharField(default='',blank=True,null=True,max_length=255)


    def __str__(self):
        return '%s' % self.name

    def get_sub_lanmu(self):
        return self.lanmu_set.all()

    def get_sup_lanmu(self):
        return self.suplanmu_set.all()

    def get_all_articals(self):
        articals = []
        for lanmu in self.get_sub_lanmu():
            for artical in lanmu.get_all_articals():
                articals.append(artical)
        return articals

    def get_all_undelete_articals(self):
        articals = []
        for lanmu in self.get_sub_lanmu():
            for artical in lanmu.get_all_undelete_articals():
                articals.append(artical)
        return articals

    def get_all_deleted_articals(self):
        articals = []
        for lanmu in self.get_sub_lanmu():
            for artical in lanmu.get_all_deleted_articals():
                articals.append(artical)
        return articals


class Suplanmu(models.Model):
    name = models.CharField(default='',blank=True,null=True,max_length=255)
    jigou = models.ForeignKey(Jigou, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    def get_sub_lanmu(self):
        return self.sub_lanmu.all()

    def get_all_articals(self):
        articals = []
        for lanmu in self.get_sub_lanmu():
            for artical in lanmu.get_all_articals():
                articals.append(artical)
        return articals

    def get_all_undelete_articals(self):
        articals = []
        for lanmu in self.get_sub_lanmu():
            for artical in lanmu.get_all_undelete_articals():
                articals.append(artical)
        return articals

    def get_all_deleted_articals(self):
        articals = []
        for lanmu in self.get_sub_lanmu():
            for artical in lanmu.get_all_deleted_articals():
                articals.append(artical)
        return articals




class Lanmu(models.Model):
    name = models.CharField(max_length=255, default='')
    jigou = models.ForeignKey(Jigou, on_delete=models.CASCADE,blank=True, null=True)
    sup_lanmu = models.ForeignKey(Suplanmu,on_delete=models.CASCADE,related_name='sub_lanmu',blank=True,null=True)


    def __str__(self):
        return '%s' % self.name

    def get_all_articals(self):
        return self.artical_set.all()

    def get_all_undelete_articals(self):
        return self.artical_set.filter(huishou=False)

    def get_all_deleted_articals(self):
        return self.artical_set.filter(huishou=True)


class Artical(models.Model):
    biaoti = models.CharField(max_length=255, default='')
    neirong = UEditorField(u'内容	', width=600, height=300, toolbars="full", imagePath="",filePath="",upload_settings={"imageMaxSize":1204000},settings={}, command=None,blank=True)
    fabiao_riqi = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(default='', blank=True, upload_to='post_images')
    yuedu = models.PositiveIntegerField(default=0,)
    dianzan = models.PositiveIntegerField(default=0,)
    file = models.FileField(default='',blank=True, upload_to='post_files')
    lanmu = models.ForeignKey(Lanmu, on_delete=models.CASCADE)
    huishou = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fabiao_riqi']

    def __str__(self):
        return '%s' % self.biaoti

    def get_absolute_url(self):
        return reverse('文章',args=(self.pk,))

    def get_delete_url(self):
        return reverse('wzDelete',args=(self.pk,))

    def is_huishou(self):
        if self.huishou:
            return True
        else:
            return False

    def get_delete_cd_url(self):
        return reverse('wzDelete_cd',args=(self.pk,))
