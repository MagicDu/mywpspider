#!/usr/bin/env python3
#-*-coding : utf-8 -*-
import pymysql
import traceback
import sys
from conf import readDBConf


#创建数据库
def createDB():
	db=readDBConf()
	conn=pymysql.connect(host=db.db_host,port=db.db_port,user=db.db_user,passwd=db.db_passwd)
	cur=conn.cursor()
	cur.execute('CREATE DATABASE IF NOT EXISTS mywpspider DEFAULT CHARSET utf8 COLLATE utf8_general_ci')
	cur.execute('use mywpspider')

	createtablesql="""CREATE TABLE spider(
		id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
		name varchar(50) DEFAULT NULL,
		url varchar(256) NOT NULL,
		urlstag varchar(255) NOT NULL,
		restr varchar(255) NOT NULL,
		newstag varchar(255) NOT NULL,
		state int(11) NOT NULL DEFAULT 0)ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8"""
	cur.execute(createtablesql)
	cur.close()
	conn.close()

#增加爬取站点配置
def addConf():
	db=readDBConf()
	conn=pymysql.connect(host=db.db_host,port=db.db_port,user=db.db_user,passwd=db.db_passwd,database='mywpspider')
	cur=conn.cursor()
	name=input('请输入抓取的站点名称：')
	url=input('请输入站点链接：')
	urlstag=input('请输入包含文章链接列表的div class属性的值：')
	restr=input('请输入匹配文章链接的正则表达式：')
	newstag=input('请输入站点包含新闻的 div class 属性值：')
	insertsql="insert into spider (name,url,urlstag,restr,newstag) values ('%s','%s','%s','%s','%s')"%(name,url,urlstag,restr,newstag)
	print(insertsql)
	try:
		cur.execute(insertsql)
		conn.commit()
	except Exception as e:
		m=traceback.format_exc()
		print(m)
		conn.rollback()
	cur.close()
	conn.close()

#执行命令行参数
def executeCommand():
	methodname=sys.argv[1]
	print(methodname)
	if methodname=='createDB':
		createDB()
	elif methodname=='addConf':
		addConf()
	else:
		print('输入错误')

executeCommand()

