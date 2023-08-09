import time
import datetime
import threading
import requests
import json



headers = {
  'authority': 'kuajing.pinduoduo.com',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9',
  'anti-content': '0aqAfqnYNjHgjgT9Q2uiaJK_Dx3thc2_X6hwYWep_qsfHgEH_8x21QZKzqpnu-FnroufoDUs9o_vcs_dtC78qKvCJIxBIOsxEQ_CtfvKjeQ6KIvvFBakF0wZWC6q2ob0mlNBEkVtzHpFz8HOXEOYuGdEcjHNK-dGc0dBIMTt-K-epPRwvXpXgRhKUnTf9oKneCZri9DXgF8y0Fbwy3nyiwnlgctL48EPP5TgKqp4SKDY14vo3bMBRCNS4TUXYwjsyDPA7T2p19ZACRBqwJy9WxMqhV0RXdOKbRVqSxgSL06GiGdd5UlYtfGNPJ3Cp36xqrwjgobqFqZHi9HLsobaZqZrRgYNaDi9loXt-IrA2FoJ-sGq1uxNmRuC1uQ37f8J8LAYRpvcf3nmHkApATc043hMDq1L-SAmVtky84Izpz1duW73bLjsGklDCrvn_ItfQ-gdw9v8_X1dKXKRy_JKUptDI5O4xukEO7VdgKuj9urLTBHJwH_0dQ-QeY9hItbxAHoEYOZH4VaTVlG2uSux9rPrSHzDihBscvL8oTmUJX3_zeuDksPRbsuHtsSn6kosOiEizaa3vZMxKOZpIaii12Lv67yWjNtH1UuhU5zkLkYS-Dvg4fAPitu04pXNGrhKllQ0azLAUIikp7kXWHWSuQDCLkeuNYlAQZaJe7K0LV2kmi2Wrt3hDZ-wPRizGMWAyDi9zQDy7TEwflq5',
  'cache-control': 'max-age=0',
  'content-type': 'application/json',
  'cookie': '_f77=43f7375e-cdd9-4bdc-b38d-319f9b278836; _bee=dNOmt1zW9VW5iwQGW0leaJWlzd98lLJl; _a42=38f0ed14-1cf3-4e1e-9bb6-0e1b12da62da; api_uid=CmmurmRcPVpYdwBaC3DQAg==; _nano_fp=XpEJXqmjn5Eal0T8lT_gBdmPI_CrAczBYbR8jaWN; rckk=dNOmt1zW9VW5iwQGW0leaJWlzd98lLJl; ru1k=43f7375e-cdd9-4bdc-b38d-319f9b278836; ru2k=38f0ed14-1cf3-4e1e-9bb6-0e1b12da62da; SUB_PASS_ID=eyJ0IjoiZHF5YjRPYVJpV3RSKzAvc2NpK0JLcnZhd1BnUU9MR3hxR0ROclAxZmk5ck0zUUdmeGxYdUZVTWdBOHp6RDc4dSIsInYiOjEsInMiOjEwMDAwLCJ1Ijo5MDQ2ODAyNDAxMzI5fQ==',
  'mallid': '634418210372218',
  'origin': 'https://kuajing.pinduoduo.com',
  'referer': 'https://kuajing.pinduoduo.com/main/order-manage',
  'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}



# 先获取 headers 

# 查询备货单列表
subPurchaseOrderSnList = []


def querySubOrderList():
  url = "https://kuajing.pinduoduo.com/oms/bg/venom/api/supplier/purchase/manager/querySubOrderList"

  payload = json.dumps({
    "pageNo": 1,
    "pageSize": 20,
    "urgencyType": 0,
    "isCustomGoods": False,
    "statusList": [
      1
    ]
  })

  response = requests.request("POST", url, headers=headers, data=payload)

  text = json.loads(response.text)

  print(text)
  if text['errorCode'] != 1000000:
    print('获取备货单列表失败，程序结束,错误消息：', text['error_msg'])
  
  result = text['result']
  subOrderForSupplierList = result['subOrderForSupplierList']

  for obj in subOrderForSupplierList:
    print(obj['subPurchaseOrderSn'])
    subPurchaseOrderSnList.append(obj['subPurchaseOrderSn'])

#拼接需要抢发货台的备货单列表
def appendJoinDeliveryPlatformRequestList(subPurchaseOrderSnList):
  # 需要添加发货台的备货单列表
  joinDeliveryPlatformRequestList = []
  for subPurchaseOrderSn in subPurchaseOrderSnList:
    # 可能有部分发货单需要删除  根据isCanJoinDeliverPlatform == true来区别是否要添加发货台
    joinDeliveryPlatformRequestList.append({"subPurchaseOrderSn":subPurchaseOrderSn})
  
  return joinDeliveryPlatformRequestList


def batchJoinDeliveryOrderPlatformV2(subPurchaseOrderSnList):
  url = "https://kuajing.pinduoduo.com/oms/bg/venom/api/supplier/purchase/manager/batchJoinDeliveryOrderPlatformV2"


  joinDeliveryPlatformRequestList = appendJoinDeliveryPlatformRequestList(subPurchaseOrderSnList)
  payload = json.dumps({"joinDeliveryPlatformRequestList":joinDeliveryPlatformRequestList})

  print("脚本开始")
  while False:

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)

    text = json.loads(response.text)

    print(text)
    print(text["success"])
    print('----------------------------')
    
    # 防止接口504 或者降级
    if text["success"] != True:
      continue

    result = text["result"]
    print(result)
    if result["isSuccess"] == True:
      break

    time.sleep(1)


  print('加入发货台成功！！！！程序结束')






  # 获取现在时间
now_time = datetime.datetime.now()
# 获取明天时间
next_time = now_time + datetime.timedelta(days=+1)
next_year = next_time.date().year
next_month = next_time.date().month
next_day = next_time.date().day
# print(next_time, next_year, next_month, next_day)
# 获取明天0点时间
next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
# print(next_time)
# # 获取昨天时间
# last_time = now_time + datetime.timedelta(days=-1)
 
# 获取距离明天0点时间，单位为秒
timer_start_time = (next_time - now_time).total_seconds()

# 如果超过0点不到1点，直接启动
if timer_start_time > 72000:
  timer_start_time = 0
print('将于', timer_start_time, '秒后开始抢发货台')
# 54186.75975
# 定时器,参数为(多少时间后执行，单位为秒，执行的方法)

timer = threading.Timer(timer_start_time, batchJoinDeliveryOrderPlatformV2,subPurchaseOrderSnList)
timer.start() 


# 然后获取备货单列表


# 批量增加发货台

# 根据仓库分别创建发货单

