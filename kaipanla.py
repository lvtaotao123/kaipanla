#coding:utf-8
import requests
import json
import time
import xlwt
import os
row = 5
def save_1(row,row1,code,name,title,time_,state,huan_shou,liu_tong,feng_dan,zhu_li,money,beca):
	ws.write(row,0,int(row1))
	ws.write(row,1,str(code))
	ws.write(row,2,str(name))
	ws.write(row,3,str(title))
	ws.write(row,4,str(time_))
	if len(state) == 1:
		ws.write(row,5,float(state))
	else:
		ws.write(row,5,state)
	ws.write(row,6,float(huan_shou))
	ws.write(row,7,float(liu_tong))
	ws.write(row,8,float(feng_dan))
	ws.write(row,9,float(zhu_li))
	ws.write(row,10,float(money))
	ws.write(row,11,str(beca))
	print('正在插入开盘啦------'+str(row-4))

def kai_pan_par1(html,ws,j):
	
	global row 
	html = json.loads(html)

	rise = '%.0f'%html['nums']['SZJS']#上涨
	fall = '%.0f'%html['nums']['XDJS']#下跌

	limit_z = '%.0f'%html['nums']['ZT']#涨停
	limit_d = '%.0f'%html['nums']['DT']#跌停

	yestRase = '%.2f'%html['nums']['yestRase']
	ZBL = '%.2f'%html['nums']['ZBL']

	data = html['list']
	if j == 0:
	
		ws.write(0,0,'上涨')
		ws.write(0,2,'涨停')
		ws.write(1,0,'下跌')
		ws.write(1,2,'跌停')
		ws.write(0,5,'昨日涨停表现（%）')
		ws.write(1,5,'破板率（%）')
		ws.write(0,1,float(rise))
		ws.write(0,3,float(limit_z))
		ws.write(0,6,float(yestRase))
		ws.write(1,1,float(fall))
		ws.write(1,3,float(limit_d))
		ws.write(1,6,float(ZBL))
		print('正在插入开盘啦------')
		ws.write(5,0,'序号')
		ws.write(5,1,'股票代码')
		ws.write(5,2,'股票名称')
		ws.write(5,3,'概念')
		ws.write(5,4,'涨停时间')
		ws.write(5,5,'状态')
		ws.write(5,6,'实际换手')
		ws.write(5,7,'实际流通')
		ws.write(5,8,'封单')
		ws.write(5,9,'主力净额')
		ws.write(5,10,'成交额')
		ws.write(5,11,'涨停原因')
	
	for item in data:
		title = item['ZSName'] #概念
		StockList = item['StockList']
		row1 = 0
		for stock in StockList:
			row1 += 1
			row +=1
			code = stock[0]#编号
			if code[0] == '0' or code[0] == '3':
				code += '.sz'
				aaa = 0
				aa = '00'
			if code[0] == '6':
				code += '.sh'
				aaa = 1
				aa = '01'
			name = stock[1]#名字
			time_arr = stock[6]#时间

			time_ = time.strftime("%H:%M:%S",time.localtime(time_arr))

			state = stock[9] #状态
			if '首板' in state:
				state = '1'
			if '连板' in state:
				state = state[0]
			money = int(stock[13])#成交额
			money = '%.4f'%(money/100000000)

			huan_shou = '%.2f'%(stock[14]) #实际换手
			liu_tong = '%.2f'%(int(stock[15])/100000000)#实际流通
			feng_dan = '%.4f'%(int(stock[8])/100000000)#封单
			zhu_li = '%.4f'%(int(stock[12])/100000000)#主力净额
			beca = stock[17]

			with open('12开盘啦个股涨停原因.txt','a') as  f:
				f.write('{}|{}|{}\n'.format(aaa,stock[0],beca))
				f.close()

			with open('tipword.txt','a') as  f:
				f.write('{}{}={}\n'.format(aa,stock[0],title))
				f.close()

			with open('mark.txt','a') as  f:
				f.write('{}{}=7\n'.format(aa,stock[0]))
				f.close()

			save_1(row,row1,code,name,title,time_,state,huan_shou,liu_tong,feng_dan,zhu_li,money,beca)
			
			'''
			print('序号：'+str(row1))
			print('代码：'+code)
			print('名字：'+name)
			print('概念：'+title)
			print('涨停时间：'+time_)
			print('状态：'+state)
			print('实际换手：'+str(huan_shou))
			print('实际流通：'+str(liu_tong))
			print('封单：'+str(feng_dan))
			print('主力净额：'+str(zhu_li))
			print('成交额：'+str(money))
			print('涨停原因：'+beca)
			print('--------------------------------------------------')
			'''
def kai_pan_par2(html,ws,row):
		html = json.loads(html)
		name = html['name']
		money = '%.2f'%html['real']['last_px']
		px_change_rate = '%.2f'%html['real']['px_change_rate']
		total_turnover = '%.0f'%(int(html['real']['total_turnover'])/100000000)
		ws.write(row,8,str(name))
		ws.write(row,9,float(money))
		ws.write(row,10,float(px_change_rate))
		ws.write(row,11,float(total_turnover))
		

def kai_pan_la(ws):
	url = 'https://hq.kaipanla.com/w1/api/index.php'

	headers = {
		
		'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; PRO 6 Plus Build/LMY48Z)',
		'Content-Length': '120',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Connection': 'Keep-Alive',
		'Host': 'hq.kaipanla.com',
		'Accept-Encoding': 'gzip',
	}

	data = [
			{'a' : 'GetPlateInfo','st' :'10','apiv':'w18','c':'DailyLimitResumption','PhoneOSNew':'1','DeviceID':'00000000-025d-1ffd-fa71-8fd5272bb997','Index':'20',},
			#{'a' : 'GetPlateInfo','st' :'10','apiv':'w18','c':'DailyLimitResumption','PhoneOSNew':'1','DeviceID':'00000000-025d-1ffd-fa71-8fd5272bb997','Index':'10',},
			{'a' : 'GetZsPanKou','apiv':'w18','c':'StockL2Data','StockID':'SH000001','PhoneOSNew':'1','UserID':'0','DeviceID':'00000000-025d-1ffd-fa71-8fd5272bb997','Token':'0',},
			{'a' : 'GetZsPanKou','apiv':'w18','c':'StockL2Data','StockID':'SZ399001','PhoneOSNew':'1','UserID':'0','DeviceID':'00000000-025d-1ffd-fa71-8fd5272bb997','Token':'0',},
			{'a' : 'GetZsPanKou','apiv':'w18','c':'StockL2Data','StockID':'SZ399006','PhoneOSNew':'1','UserID':'0','DeviceID':'00000000-025d-1ffd-fa71-8fd5272bb997','Token':'0',}
			]
	j = 0
	while True:
		
		index = str(j*10)
		data[0]['Index'] = index
		html = requests.post(url, headers=headers,data = data[0])
		#print(len(html.text))
		html1 = html.text.encode('utf-8').decode("utf-8",'ignore')
		html33 = json.loads(html1)
		
		#print(html1)
		
		if len(html33['list']) == 0:
			break
		kai_pan_par1(html1,ws,j)
		j += 1
		time.sleep(0.1)

	for i in range(1,4):
		html2 = requests.post(url, headers=headers,data = data[i]).text
		html2 = html2.encode('utf-8').decode("utf-8",'ignore')
		kai_pan_par2(html2,ws,i-1)
if __name__ == '__main__': 
	wb = xlwt.Workbook()
	ws = wb.add_sheet('开盘啦')
	if os.path.exists('12开盘啦个股涨停原因.txt'):
		os.remove('12开盘啦个股涨停原因.txt')
	if os.path.exists('tipword.txt'):
		os.remove('tipword.txt')
	if os.path.exists('mark.txt'):
		os.remove('mark.txt')
	kai_pan_la(ws)
	wb.save('开盘啦复盘.xls')

'''
apiv	w18
c	DailyLimitResumption
PhoneOSNew	1
DeviceID	00000000-025d-1ffd-fa71-8fd5272bb997
Index	0


https://hq.kaipanla.com/w1/api/index.php

a	GetZsPanKou
apiv	w18
c	StockL2Data
StockID	SH000001
PhoneOSNew	1
UserID	0
DeviceID	00000000-025d-1ffd-fa71-8fd5272bb997
Token	0

https://hq.kaipanla.com/w1/api/index.php
a	GetZsPanKou
apiv	w18
c	StockL2Data
StockID	SZ399001
PhoneOSNew	1
UserID	0
DeviceID	00000000-025d-1ffd-fa71-8fd5272bb997
Token	0


https://hq.kaipanla.com/w1/api/index.php
a	GetZsPanKou
apiv	w18
c	StockL2Data
StockID	SZ399006
PhoneOSNew	1
UserID	0
DeviceID	00000000-025d-1ffd-fa71-8fd5272bb997
Token	0

'''