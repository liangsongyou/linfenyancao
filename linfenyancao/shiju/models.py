from django.db import models
from django.urls import reverse
from django.shortcuts import  get_object_or_404

# Create your models here.
class Lanmu(models.Model):
    name = models.CharField(max_length=255, default='')

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

