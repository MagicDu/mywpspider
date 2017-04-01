#!/usr/bin/env python3
#-*-coding : utf-8 -*-
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.methods.posts import GetPosts,NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from email.mime.text import MIMEText
from email.header import Header
import re
import time
import smtplib
import traceback
import os,random
import requests
import sys
from conf import *
from myutils import *

user_agents=load_user_agent()

#新闻类
class News(object):
	def __init__(self,title,tags,category,content,image_name):
		self.title = title     #标题
		self.tags=tags         #标签
		self.category=category #分类
		self.content=content   #内容
		self.image_name=image_name


#设置请求头
def setHeader(url):
	#抽取URL中的主机名
	host=url.replace('http://','')
	length = len(user_agents)
	index=random.randint(0,length-1)
	user_agent = user_agents[index]
	headers={
		'Referer': url,
		'Host':host,
		'User-Agent':user_agent,
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}
	return headers


#获取最新的新闻链接列表

'''
url  :需要抓取的网址
n    :获取链接的数量,即每次需要发布新文章的数量
links:返回链接列表
'''
def get_urls(url,classname,restr,n=1):
	links=[]
	headers=setHeader(url)
	bsObj=requests.session()
	bsObj=BeautifulSoup(bsObj.get(url,headers=headers).content,'html.parser')
	#print(bsObj.find('div',{'class':classname}))
	for link in bsObj.find('div',{'class':classname}).findAll('a')[0:n]:
		if 'href' in link.attrs:
			href=link.attrs['href']
			#print(href)
			if href.startswith('//'):
				href='http:'+href
			elif href.startswith('/'):
				href=url+href
			if re.match(restr,href):
				links.append(href)
	return links



def get_news(url,link,classname):
	headers=setHeader(url)
	bsObj=requests.session()
	art=bsObj.get(link,headers=headers)
	print(art.status_code)
	bsObj=BeautifulSoup(art.content,'html.parser')
	tit=bsObj.h1
	if tit!=None:
		title=tit.get_text()
	else:
		title=bsObj.title.get_text()
	print(title)
	tags_list=bsObj.find('meta',{'name':'keywords'}).attrs['content']
	#print(tags_list)
	l=re.split(',',tags_list)
	tags=[item for item in filter(lambda x:x != '', l)]
	category="其他"
	#查找图片
	a_tag=content.find('img')
	if a_tag!=None and a_tag.attrs['src']!='':
		image_url=a_tag.attrs['src']
		image_name=os.path.basename(image_url).split('!')[0]
		print(image_url)
		#下载图片
		get_image(image_url,image_name)
		#删除标签
		a_tag.extract()
	else:
		image_name=''
	news=News(title,tags,category,content.prettify(),image_name)
	return news

#发送新闻到wordpress

'''
user:用户对象
news:新闻对象
'''

def send_news(user,news):
	wp=Client(user.website,user.username,user.password)
	post=WordPressPost()
	if news.image_name!='':
		attachment_id=upload_image(news.image_name,wp)
		post.thumbnail = attachment_id
	post.title=news.title
	post.content=news.content
	post.post_status ='publish'
	post.terms_names={
		'post_tag':news.tags,
		'category':[news.category]
	}
	wp.call(NewPost(post))


user=readUserConf()
l=getConf()
if len(l)==0:
	print('对不起，还没有配置抓取的站点信息')
	sys.exit()
for conf in l:
	url=conf.url
	classname=conf.urltag
	newstag=conf.newstag
	restr=conf.restr
	ulist=get_urls(url,classname,restr,1)
	for ul in ulist:
		print(ul)
		try:
			news=get_news(url,ul,newstag)
			write_file(news.title+'\n')
			send_news(user,news)
			time.sleep(5)
		except Exception as e:
			m=traceback.format_exc()
			print(m)
			send_email(m)
			print('抓取失败：'+ul)
			continue