from django.db import models
from django.urls import reverse
from django.shortcuts import  get_object_or_404

# Create your models here.
class Jigou(models.Model):
    name = models.CharField(default='',blank=True,null=True,max_length=255)


    def __str__(self):
        return '%s' % self.name

    def get_sub_lanmu(self):
        return self.lanmu_set.all()

    def get_sup_lanmu(self):
        return self.suplanmu_set.all()


class Suplanmu(models.Model):
    name = models.CharField(default='',blank=True,null=True,max_length=255)
    jigou = models.ForeignKey(Jigou, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    def get_sub_lanmu(self):
        return self.sub_lanmu.all()


class Lanmu(models.Model):
    name = models.CharField(max_length=255, default='')
    jigou = models.ForeignKey(Jigou, on_delete=models.CASCADE,blank=True, null=True)
    sup_lanmu = models.ForeignKey(Suplanmu,on_delete=models.CASCADE,related_name='sub_lanmu',blank=True,null=True)


    def __str__(self):
        return '%s' % self.name


class Artical(models.Model):
    biaoti = models.CharField(max_length=255, default='')
    neirong = models.TextField(default='',blank=True)
    fabiao_riqi = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(default='', blank=True, upload_to='post_images')
    yuedu = models.PositiveIntegerField(default=0,)
    dianzan = models.PositiveIntegerField(default=0,)
    file = models.FileField(default='',blank=True, upload_to='post_files')
    lanmu = models.ForeignKey(Lanmu, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.biaoti

    def get_absolute_url(self):
        return reverse('文章',args=(self.pk,))

