#!/usr/bin/python
#coding:utf-8

import extractDataToDatabase

'''
有可能有部分书籍没有统计完成，所以，在TOP30里面再查找一次，
没有的部分再加入到最终的书籍里面
'''

def getFinalBookInfo():
    top30 = extractDataToDatabase.getFileContainsBooks('index.html')
    allbooks = extractDataToDatabase.getDirData('./books/')
    for book in top30:
        bookName = book['name']
        bookFind = False
        for allBook in allbooks:
            if allBook['name'] == bookName:
                bookFind = True
                break

        if bookFind == False:
            allbooks.append(book)

    return allbooks


if __name__ == "__main__":
    totalBooksInfo = getFinalBookInfo()
    extractDataToDatabase.writeDataToTheDB(totalBooksInfo)
