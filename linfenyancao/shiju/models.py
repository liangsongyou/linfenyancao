from datetime import date

from django.db import models
from django.urls import reverse
from django.shortcuts import  get_object_or_404, redirect
from django.contrib.auth.models import User

from DjangoUeditor.models import UEditorField

# Create your models here.
class Jigou(models.Model):
    name = models.CharField(default='',blank=True,null=True,max_length=255)
    telephone = models.CharField(default='',blank=True,null=True,max_length=255)
    email = models.CharField(default='',blank=True,null=True,max_length=255)


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

    def get_absolute_url(self):
        return reverse('xianju',args=[self.pk])

    def get_xianju_url(self):
        return reverse('xianju',args=[self.pk])

    def get_keshi_url(self):
        return reverse('keshi',args=[self.pk])


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

    def get_first_ten_articals(self):
        if len(self.get_all_undelete_articals()) > 10:
            return self.get_all_undelete_articals()[:10]
        else:
            return self.get_all_undelete_articals()


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
        return reverse('artical',args=(self.pk,))

    def get_delete_url(self):
        return reverse('wzDelete',args=(self.pk,))

    def is_huishou(self):
        if self.huishou:
            return True
        else:
            return False

    def get_delete_cd_url(self):
        return reverse('wzDelete_cd',args=(self.pk,))


class Profile(models.Model):
    ZHI_BAN_DATE = (
        ('0','星期一'),
        ('1','星期二'),
        ('2','星期三'),
        ('3','星期四'),
        ('4','星期五'),
        ('5','星期六'),
        ('6','星期日'),
        ('7','无'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True)
    display_name = models.CharField(default='',max_length=100)
    zhiwei = models.CharField(default='',max_length=100)
    zhiban_date = models.CharField(max_length=10,
                                   choices=ZHI_BAN_DATE,
                                   default='7',)
    jigou = models.ForeignKey(Jigou, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return '%s' % self.display_name

    @property
    def is_zhiban(self):
        return int(self.zhiban_date) == date.today().weekday()






































