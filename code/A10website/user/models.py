# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField


class UserProfile(AbstractUser):

    ROLE_CHOICES = (
        (0, u"admin"),
        (1, u"dataManager"),
        (2,u'user')
    )

    name = models.CharField(max_length=255,blank=True, null=True, verbose_name='昵称')
    avatar = ProcessedImageField(upload_to='avatar', blank=True, null=True, default='static/avatar/default.jpg', verbose_name='头像')
    roles = models.IntegerField(choices=ROLE_CHOICES, default=2, blank=True, null=True,)
    introduction = models.CharField(max_length=255,blank=True, null=True, verbose_name='用户简介')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


