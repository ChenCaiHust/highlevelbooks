#coding:utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.
#
# 存储图书的分类
class Catogray(models.Model):
	##图书类别的文字表示
	type = models.CharField(max_length=32, unique=True)
	
	def __unicode__(self):
		return self.type

#
#存储具体的图片信息
class BooksInfo(models.Model):
	name = models.CharField(max_length=128, unique=True)
	authur = models.CharField(max_length=128)
	pictureName = models.CharField(max_length=64)
	mentionedTimes = models.IntegerField()
	type = models.CharField(max_length=32)
	introduction = models.TextField()
	jd = models.CharField(max_length=512)
	dangdang = models.CharField(max_length=512, null=True)
	
	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category', args=[self.type + '.html'])