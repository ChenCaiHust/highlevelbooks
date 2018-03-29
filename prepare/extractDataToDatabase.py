#!/usr/bin/python
#coding:utf-8

from lxml import etree
from stackoverflow.wsgi import *
from mysite.models import Catogray, BooksInfo
import chardet
import os


'''
get extract file names
'''
def getExtractFileNames(path):
	fileList = os.listdir(path)
	return fileList
	
'''
get the valuable content
'''
def filterTheFileFirstTime(fileName):
	output = ''
	f = open(fileName)
	content = ''
	brComming = False
	footerComming = False
	for line in f:
		if line.find(r'<br') > 0:
			brComming = True
			continue
		if line.find('footer class') > 0:
			footerComming = True
			break
		
		if brComming == True and footerComming == False:
			content = content + line
	
	content = content.decode('gbk')
	f.close()
	output += content
	return output

'''
write the data to list(dict construct)
'''
def getBooksList(content):
	booksList = []
	tempList = []
	imgList = []
	
	#construct html etree
	html = etree.HTML(content)

	#get image
	pictureresult = html.xpath('//div[@class="row"]//img')
	for element in pictureresult:
		picName = element.get('src')
		picName = picName[4:]
		bookpic = {'pictureName' : picName}
		imgList.append(bookpic)

	#get bookname
	booknameresult = html.xpath('//div[@class="row"]/div/h2')
	for element in booknameresult:
		#extract Bookname
		bookName = {'name' : element.text}
		tempList.append(bookName)

		#extract bookAuthur
		authur = element.getnext()
		bookAuthur = {'authur' : authur.text}
		tempList.append(bookAuthur)
		
		#extract times
		metiontimes = authur.getnext()
		bookMetainTimes = {'mentionedTimes' : metiontimes.text.split(' ')[1]}
		tempList.append(bookMetainTimes)
		
		links = ''
		#get introduction
		bookIntroductionText = ''
		loopVariable = metiontimes.getnext()
		condition = True
		while condition:
			if (loopVariable.text != None):
				bookIntroductionText += loopVariable.text + '\n'
				loopVariable = loopVariable.getnext()
			else:
				links = loopVariable
				condition = False
		
		bookIntroduction = {'introduction' : bookIntroductionText}
		tempList.append(bookIntroduction)
		
		#get links
		linksresult = links.getchildren()
		jdLinks = {'jd' : linksresult[0].get('href')}
		tempList.append(jdLinks)
		if len(linksresult) == 2:
			ddLinks = {'dangdang': linksresult[1].get('href')}
			tempList.append(ddLinks)
		booksList.append(tempList)
		tempList = []

	for i in range(len(booksList)):
		booksList[i].append(imgList[i])
	
	newBookList = []
	newTempBookList = {}
	
	for book in booksList:
		for section in book:
			for key in section:
				newTempBookList[key] = section[key]
		newBookList.append(newTempBookList)
		newTempBookList = {}
	
	return newBookList

def checkStrEncodingType(string):
	import chardet
	fencoding=chardet.detect(string)
	print fencoding
	return fencoding

def writeDataToTheDB(totalBooksInfo):
	path = './books/'
	fileNames = getExtractFileNames(path)
	alltheTypes = []
	for file in fileNames:
		alltheTypes.append(file.split('.')[0])
		
	#construct typename
	for typaName in alltheTypes:
		row = Catogray.objects.get_or_create(type=typaName)[0]
		
	
	#write the books info into database
	for bookInfo in totalBooksInfo:
		dangdanglink = bookInfo.get('dangdang','')
		##print(bookInfo)
		row = BooksInfo.objects.get_or_create(
			name=bookInfo['name'],
			authur=bookInfo['authur'],
			pictureName=bookInfo['pictureName'],
			mentionedTimes=bookInfo['mentionedTimes'],
			type=bookInfo['type'],
			introduction=bookInfo['introduction'],
			jd=bookInfo['jd'],
			dangdang=dangdanglink)[0]
			


def getDirData(dirPath):
	path = dirPath
	fileNames = getExtractFileNames(path)
	totalFileInfo = []
	for file in fileNames:
		realFileName = path + file
		fileContent = filterTheFileFirstTime(realFileName)
		bookType = file.split('.')[0]

		booksList = getBooksList(fileContent)
		for book in booksList:
			book["type"] = bookType
			totalFileInfo.append(book)
	return totalFileInfo

def getFileContainsBooks(fileName):
	totalFileInfo = []
	fileContent = filterTheFileFirstTime(fileName)
	booksList = getBooksList(fileContent)
	for book in booksList:
		book["type"] = 'alwaysgoodbooks'
		totalFileInfo.append(book)
	return totalFileInfo

#writeDataToTheDB(totalFileInfo)
