#!/usr/bin/env python3
#-*-coding : utf-8 -*-
from urllib.request import urlretrieve
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import traceback
import os,re

from conf import readEmailConf

# 根据url 获取主机名
def getHost(url):
    reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
    m = re.match(reg, url)
    uri = m.groups()[0] if m else ''
    host=uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
    return host


#加载user_agents配置文件
def load_user_agent():
	user_agents=[]
	fp = open('user_agents', 'r')
	line  = fp.readline().strip('\n')
	while(line):
		user_agents.append(line)
		line = fp.readline().strip('\n')
	fp.close()
	return user_agents

#下载图片
'''
将图片保存到本地
'''
def get_image(image_url,image_name):
	os.makedirs('images',exist_ok=True)
	#print('下载了--->'+image_name)
	urlretrieve(image_url,'images/'+image_name)

#上传图片
'''
根据图片路径将图片上传到wordpress

返回attachment_id
'''
def upload_image(image_name,client):
	data={
		'name':image_name,
		'type':'image/jpeg'
	}
	with open('images/'+image_name, 'rb') as img:
		data['bits'] = xmlrpc_client.Binary(img.read())
	response = client.call(media.UploadFile(data))
	#print('上传了--->'+image_name)
	attachment_id = response['id']
	return attachment_id


#将文章标题写入文件
def write_file(str_title):
	with open('title.txt','a') as f:
		f.write(str_title)


#发送电子邮件
'''
mail_user   :发送者名称
mail_postfix:邮箱后缀
sender      :发送者
receiver    :接收者(可以设置为139邮箱)
smtpserver  :smtp服务器地址
message     :消息
subject     :主题
username    :用户名
password    :密码
example: 以新浪邮箱为例
send_email('user','sina.com','user@sina.com','xxxx@qq.com','smtp.sina.com','您的爬虫出现异常\n'+m,'wpspider','user@sina.com','abc123')
'''

def send_email(m):
	email=readEmailConf()
	try:
		msg=MIMEText(email.message+m,'plain','utf-8')
		me="Wpspider"+"<"+email.mail_user+"@"+email.mail_postfix+">" 
		msg['From']=Header(me)
		msg['Subject']=Header(email.subject,'utf-8')
		smtp = smtplib.SMTP()
		smtp.connect(email.smtpserver)
		smtp.login(email.username,email.password)
		smtp.sendmail(email.sender, email.receiver, msg.as_string())
		smtp.quit()
		print ("邮件发送成功")
	except smtplib.SMTPException as e:
		print ("Error: 无法发送邮件")
	