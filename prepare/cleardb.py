#!/usr/bin/python
#coding:utf-8

###clear database for developing
###
from stackoverflow.wsgi import *
from mysite.models import Catogray, BooksInfo

'''
问题：如果数据库模式改变后，写不进去数据，之前的数据不想要了，如何处理比较方便？
答案：
1. 把之前的数据库内容清除掉
2. 在APP里面的migrations目录下面删除__init__.py以外的所有文件
3. 运行manage.py makemigrations
4. 运行manage.py migrate
'''

def clearDb():
    ## clear Catogray db
    result = Catogray.objects.all().delete()
    print(result)

    ## clear books info db
    result = BooksInfo.objects.all().delete()
    print(result)

if __name__ == "__main__":
    clearDb()