import time
import datetime
import threading
import requests
import json


url = "https://kuajing.pinduoduo.com/oms/bg/venom/api/supplier/purchase/manager/batchJoinDeliveryOrderPlatformV2"


payload = json.dumps({
  "joinDeliveryPlatformRequestList": [
    {
      "subPurchaseOrderSn": "WB230807960080"
    },
    {
      "subPurchaseOrderSn": "WB230807806868"
    },
    {
      "subPurchaseOrderSn": "WB230807832343"
    },
    {
      "subPurchaseOrderSn": "WB230807158872"
    },
    {
      "subPurchaseOrderSn": "WB230807492336"
    },
    {
      "subPurchaseOrderSn": "WB230807432592"
    }
  ]
})
headers = {
  'authority': 'kuajing.pinduoduo.com',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9',
  'anti-content': '0aqWfqlygiKy89v9T9o3hE5_vwTSFeN42JefMSdk6nnlIcOmIbbr7ZJFc5MDAeyLAHvckbGDh8FtFgJzQKtZU2S-eG5WTPFwi60mZeg_Dxhho1SIJVwwzt6Y5XoVitUNmJJNd8DPMd0MuylG0nYFx_3jSDlmFPjpMmKXY9CfmCKkEVdfmTyPUpUkP3R0y7lJG6CwvvUA363bxp1KU7y_SR9fEpztVxty9fNVRFds4S24-dwO8VlTwWHN27AV5evd-XFgoq9IRZcR9EJyuWwk3LUXL6PogzCweS35AmZ9-nIvQwUEBdGL4fD_kAV5SML3UdYBo8gHI0XufM3ueK50mU4TsqYYXxecbftJA3GH1RMqfTCQtVQQ7mmqCwhUKcS-06AjsxfJexFX0qhOfEVgK1hu-eIKIDu4uzvll7kp7MIBuL_Wby6_Joq7riorBNdks65ketuPeh58RJ1A91p1q4LTmx6FVExwXbSlsOopF1QYbjd77oPQIemZOf3EdYH4QfHjFpDiwAeVECxEpa7fXBXYv15Qihmd21Iv0yqIlhujqQrT2XHBQaT0QJCq_1LEBErj60uDMAiOkpzv0-2aPMce9N1vp7-HrCF6D6FJKBwl3wjFbFxFbiyMXr0MMJcyqG4gvY3YW2Kk-wJZkB2bStCTQtLiimpIMymG1C7mAEk8h0lmmLgnWbT6ham6ZrkKyYO0O_n5RtzhHoSlU85fZuI7RKX34N_OQGFBgpdOVt',
  'cache-control': 'max-age=0',
  'content-type': 'application/json',
  'cookie': '_bee=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; _f77=6f8352db-3d3b-4d22-840b-a7ea88876cc2; _a42=4f526040-7d9d-4151-bcec-b86be9d48bf9; api_uid=CmlqNWRGQQUDawBThno0Ag==; _nano_fp=XpEJX5Xxnpmjn0d8nC_gtoIgd1lWrNnWYuYin1UJ; rckk=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; ru1k=6f8352db-3d3b-4d22-840b-a7ea88876cc2; ru2k=4f526040-7d9d-4151-bcec-b86be9d48bf9; SUB_PASS_ID=eyJ0IjoiQWs1T1RjWXljN00yaCthNGU0SHkrNWQvS1B5V1BNcVIzbnNhZ1I5QWpvU3R2RzFFNmZtWGI5K25mSUVzU0FwRyIsInYiOjEsInMiOjEwMDAwLCJ1Ijo5MDQ2ODAyNDAxMzI5fQ==',
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


def func():
  print("脚本开始")
  while True:

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

timer = threading.Timer(timer_start_time, func)
timer.start() 