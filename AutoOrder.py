import time
import datetime
import threading
import requests
import json


headers = {
  'authority': 'kuajing.pinduoduo.com',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9',
  'anti-content': '0aqWtxUkM_VetKO8nfLM2Epz5L6sJfiY0ikXIJ5ehZZCOrqBvUJnUiULzKlK1RaX9gpCuqT7XegLwSngjSQ9hMtYTAkgIrUe-U0CtE-414heiS6NZ3fo8kkYlGLSKoZQhcv-c-9WUtmlNOMfX8tHkS-4t9RaTDCRdLwTOT8M2FHMTrgCPVgBNlZc-L77y4L6AcM-Vi9hKJcnFor_5L61Lao7We4LpQOJjM89QMjHTiedVT1GDYlH9R4A4AHGRcJflJ08OmDca-scrlhJaq5hjSTVhStHs29iPd7E84LBhosXzan550oSiJ6xmgoULI4ZE-6pv-4Ok7RCSk1e-kMEH1Ww7kWpMFRsQF-3RCI3qkM3hSSBL7FBhSMthe-1ICI-ZD-1Re-zYGOCmQ3YGB439QEZ3qtODMtFDMZOm645D71ZD7kHI6k1D6BKe7BFD71M7B9VyTsN5uAkKMzMk7BU4E3oo-zMdF35CIMWVeG6hB982XX5xENwZwngCwnH4799MeMjVKzk5DD0KbB4dM1bD-tJ1F-RIm63SH6kVKDJZbZoUbL0UMk8DFGrISt8CMD0Obk_CM3ICI6ZF9dwz9ZQgscOpVdIIz4fLX9jpo0lGf5Hq9JGNNVxpXTQdLitlNYTuvatrYfXqNNOUwqnNNajGhgDtvdiT0P7SBIpv-QIS3xkFMIX5VsByVb3RevRKvPhwu6ZHKF-UhBkQd-6Y5M8iIh-lY68TS0VvCU9Vn9OVYFA4ZsFrf2',
  'cache-control': 'max-age=0',
  'content-type': 'application/json',
  'cookie': '_bee=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; _f77=6f8352db-3d3b-4d22-840b-a7ea88876cc2; _a42=4f526040-7d9d-4151-bcec-b86be9d48bf9; api_uid=CmlqNWRGQQUDawBThno0Ag==; _nano_fp=XpEJX5Xxnpmjn0d8nC_gtoIgd1lWrNnWYuYin1UJ; rckk=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; ru1k=6f8352db-3d3b-4d22-840b-a7ea88876cc2; ru2k=4f526040-7d9d-4151-bcec-b86be9d48bf9; SUB_PASS_ID=eyJ0IjoiejJvb3V6TkMzVS9oM0NKT1dNMkZrKzJ4UmZrcEh2RnRzV1QvYUlEWWM5di9FclFIbWk0NXBPOWZvWGltZXFhTyIsInYiOjEsInMiOjEwMDAwLCJ1Ijo5MDQ2ODAyNDAxMzI5fQ==',
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


# 备货单列表
subPurchaseOrderSnList = []
delay_sec = 5

# 查询备货单列表
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

  if 'error_code' in text:
    # 有 error_code 说明网关层面异常，现在遇到的有token过期
    print(text)

  if text['success'] != True:
    print('获取备货单列表失败，程序结束,错误消息：', text['error_msg'])
  
  result = text['result']
  subOrderForSupplierList = result['subOrderForSupplierList']

  for obj in subOrderForSupplierList:
    print(obj['subPurchaseOrderSn'])
    subPurchaseOrderSnList.append(obj['subPurchaseOrderSn'])

def excludeSubPurchaseOrderSnList(excludeSubPurchaseOrderSnList):
  for subPurchaseOrderSn in excludeSubPurchaseOrderSnList:
    subPurchaseOrderSnList.remove(subPurchaseOrderSn)


#拼接需要抢发货台的备货单列表
def appendJoinDeliveryPlatformRequestList(subPurchaseOrderSnList):
  # 需要添加发货台的备货单列表
  joinDeliveryPlatformRequestList = []
  for subPurchaseOrderSn in subPurchaseOrderSnList:
    # 可能有部分发货单需要删除  根据isCanJoinDeliverPlatform == true来区别是否要添加发货台
    joinDeliveryPlatformRequestList.append({"subPurchaseOrderSn":subPurchaseOrderSn})
  
  return joinDeliveryPlatformRequestList

def checkResponseAndReturnJson(response):
  text = json.loads(response.text)
  if 'error_code' in text:
    # 有 error_code 说明网关层面异常，现在遇到的有token过期
    print('checkResponseAndReturnJson:',text)  
  return text

# 批量抢发货台
def batchJoinDeliveryOrderPlatformV2():
  url = "https://kuajing.pinduoduo.com/oms/bg/venom/api/supplier/purchase/manager/batchJoinDeliveryOrderPlatformV2"


  joinDeliveryPlatformRequestList = appendJoinDeliveryPlatformRequestList(subPurchaseOrderSnList)
  payload = json.dumps({"joinDeliveryPlatformRequestList":joinDeliveryPlatformRequestList})

  print("脚本开始")
  while True:

    response = requests.request("POST", url, headers=headers, data=payload)

    text = checkResponseAndReturnJson(response)
    
    # 防止接口504 或者降级
    if text["success"] != True:
      print(text["success"],' reason:',text['errorMsg'])
      print('----------------------------')
      time.sleep(delay_sec)
      continue

    result = text["result"]
    print(result)
    if result["isSuccess"] == True:
      break
    else:
      time.sleep(delay_sec)


  print('加入发货台成功！！！！程序结束')

 # 输入
def startTimer(day,hour):
  if day == 0 and hour == 0:
    batchJoinDeliveryOrderPlatformV2()
  else:
    # 获取现在时间
    now_time = datetime.datetime.now()
    # 获取明天时间
    next_time = now_time + datetime.timedelta(days=+day)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # print(next_time, next_year, next_month, next_day)
    # 获取明天0点时间
    next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " "+str(hour)+":00:00", "%Y-%m-%d %H:%M:%S")
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

    timer = threading.Timer(timer_start_time, batchJoinDeliveryOrderPlatformV2)
    timer.start() 



## 这个功能需要解决anti-content的问题
def pageQuerySubPurchaseOrder():
  url = "https://kuajing.pinduoduo.com/bgSongbird-api/supplier/deliverGoods/platform/pageQuerySubPurchaseOrder"

  payload = json.dumps({
    "pageNo": 1,
    "pageSize": 100
  })

  response = requests.request("POST", url, headers=headers, data=payload)
  text = checkResponseAndReturnJson(response)

  if text["success"] == True:
    result = text["result"]
    list = result['list']



















##########################################################主程序

# 这段必须要执行
# querySubOrderList()
# excludeSubPurchaseOrderSnList(['WB230808050823'])

subPurchaseOrderSnList = ['WB2308111560520','WB230813258024']
# batchJoinDeliveryOrderPlatformV2()
startTimer(0,0)