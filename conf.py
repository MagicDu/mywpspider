#!/usr/bin/env python3
#-*-coding : utf-8 -*-
import pymysql
import traceback
import configparser
#站点配置类
class Conf(object):
	def __init__(self,id,name,url,urltag,restr,newstag):
		self.id=id
		self.name=name		#抓取的网站名
		self.url=url   		#抓取的链接
		self.urltag=urltag  #url列表div对应的class 属性名
		self.restr=restr    #匹配文章链接的正则表达式
		self.newstag=newstag#抓取文章内容时包含文章内容的div对应的class属性名
#用户配置类
class User(object):
	def __init__(self,website,username,password):
		self.website=website	#用户站点
		self.username=username	#站点用户名
		self.password=password	#站点密码

class Db(object):
	def __init__(self,db_host,db_port,db_user,db_passwd):
		self.db_host = db_host
		self.db_port=db_port
		self.db_user=db_user
		self.db_passwd=db_passwd

class Email(object):
	def __init__(self, mail_user,mail_postfix,sender,receiver,smtpserver,message,subject,username,password):
		self.mail_user = mail_user
		self.mail_postfix=mail_postfix
		self.sender=sender
		self.receiver=receiver
		self.smtpserver=smtpserver
		self.message=message
		self.subject=subject
		self.username=username
		self.password=password
		
#读取数据库配置文件
def readDBConf():
	cf = configparser.ConfigParser()
	cf.read('wp.conf')
	db_host = cf.get("db", "db_host")
	db_port = cf.getint("db", "db_port")
	db_user = cf.get("db", "db_user")
	db_passwd = cf.get("db", "db_passwd")
	db=Db(db_host,db_port,db_user,db_passwd)
	return db

#读取WordPress站点配置
def readUserConf():
	cf = configparser.ConfigParser()
	cf.read('wp.conf')
	website=cf.get('web','website')
	username=cf.get('web','username')
	password=cf.get('web','password')
	user=User(website,username,password)
	return user

#读取email配置
def readEmailConf():
	cf = configparser.ConfigParser()
	cf.read('wp.conf')
	mail_user = cf.get('email','mail_user')
	mail_postfix=cf.get('email','mail_postfix')
	sender=cf.get('email','sender')
	receiver=cf.get('email','receiver')
	smtpserver=cf.get('email','smtpserver')
	message=cf.get('email','message')
	subject=cf.get('email','subject')
	username=cf.get('email','username')
	password=cf.get('email','password')
	email=Email(mail_user,mail_postfix,sender,receiver,smtpserver,message,subject,username,password)
	return email
#从数据库加载配置
#user:数据库用户名
#passwd:数据库密码

def getConf():
	db=readDBConf()
	conn=pymysql.connect(host=db.db_host,port=db.db_port,user=db.db_user,passwd=db.db_passwd,database='mywpspider')
	cur=conn.cursor()
	cur.execute('select * from spider where state=0')
	l=cur.fetchall()
	confList=[]
	for s in l:
		id=s[0]
		name=s[1]
		url=s[2]
		urltag=s[3]
		restr=s[4]
		newstag=s[5]
		spider=Conf(id,name,url,urltag,restr,newstag)
		confList.append(spider)
	cur.close()
	conn.close()
	return confList