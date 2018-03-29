#!/usr/bin/python
#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from .models import Catogray, BooksInfo
from django.forms.models import model_to_dict

# Create your views here.
def index(request):
	top30 = BooksInfo.objects.all().order_by('-mentionedTimes')[:30]
	return render(request, 'mysite/index.html', getBooksInfo(top30))


def bookCategory(request, category):
	result = category.split('.')[0]
	books = BooksInfo.objects.filter(type=result)
	if len(books) == 0:
		top30 = BooksInfo.objects.all().order_by('-mentionedTimes')[:30]
		return render(request, 'mysite/index.html', getBooksInfo(top30))
	else:
		return render(request, 'mysite/index.html', getBooksInfo(books))

'''
获取图书列表，做这一步处理是为了页面上的介绍信息分段显示
'''
def getBooksInfo(books):
	booksList = []
	for book in books:
		bookDict = model_to_dict(book)
		bookIntrduction = bookDict['introduction']
		introList = bookIntrduction.split('\n')
		bookDict['introduction'] = introList
		booksList.append(bookDict)
	return {'booksList': booksList}