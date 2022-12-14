#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
import json
import datetime
import time
from gateAPI import GateIO

# 填写 APIKEY APISECRET
apikey = '86B14740-2363-45F5-86DD-6EACCD3CB1C8'
secretkey = 'da021582cd193190cba4c140932076e604a6a49b66d13e9e47670d67c03f537c'
API_URL = 'data.gate.io'


gate = GateIO(API_URL,apikey,secretkey)


# 所有交易对
#print (gate.pairs())


# 市场订单参数
# print (gate.marketinfo())


# 交易市场详细行情
# print (gate.marketlist())


# 所有交易行情
#print (gate.tickers())


# 单项交易行情
#print (gate.ticker('doge_usdt'))



# 所有交易对的市场深度
# print (gate.orderBooks())


# 单项交易对的市场深度
print (gate.orderBook('doge_usdt'))
data  = gate.orderBook('doge_usdt')
#for element in data['asks']:
#	print (element)
print (data['asks'][0])

# 单项交易对的市场深度
# print (gate.tradeHistory('btc_usdt'))

# 获取账号资金
#print (gate.balances())
a=0;
data = gate.balances()
data=json.loads(data)
print(data)
for item in data:
    print (item)
print (data['available'] == [])

while True:
	data = gate.balances()
	data=json.loads(data)
	if data['available'] != []:
		print(datetime.datetime.utcnow())
		print(data['available']['EOS'])
		break
	else:
		time.sleep(60)


# 获取充值地址
# print (gate.depositAddres('btc'))

# 获取充值提现历史记录
# print (gate.depositsWithdrawals('1469092370','1569092370'))


# 下单交易买入
# print (gate.buy('etc_btc','0.001','123'))

# 下单交易买入
# print (gate.sell('etc_btc','0.001','123'))


# 取消下单
# print (gate.cancelOrder('267040896','etc_btc'))

# 取消所有订单
# print (gate.cancelAllOrders('0','etc_btc'))


# 获取下单状态
# print (gate.getOrder('267040896','eth_btc'))


# 获取下单状态
# print (gate.openOrders())

# 获取我的24小时内成交记录
# print (gate.mytradeHistory('etc_btc','267040896'))


# 提现
# print (gate.withdraw('btc','88','your address'))
