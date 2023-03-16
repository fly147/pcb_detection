from django.db import models

class User(models.Model):
    '''用户表'''
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=256)
    is_superuser = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Check(models.Model):
    check_time = models.DateField(null=True,blank=True,verbose_name='检测时间')
    check_pepole = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,verbose_name='检测人员')
    origin_picture = models.CharField(max_length=256,verbose_name='原始图片')
    check_picture = models.CharField(max_length=256,verbose_name='检测图片')

    class Meta:
        verbose_name = 'PCB检测信息'
        verbose_name_plural = 'PCB检测信息'
