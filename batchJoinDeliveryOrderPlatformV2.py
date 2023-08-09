import time
import datetime
import threading
import requests
import json


url = "https://kuajing.pinduoduo.com/oms/bg/venom/api/supplier/purchase/manager/batchJoinDeliveryOrderPlatformV2"


payload = json.dumps({
  "joinDeliveryPlatformRequestList": [{"subPurchaseOrderSn":"WB230808477534"},{"subPurchaseOrderSn":"WB230808050823"}]
})
headers = {
  'authority': 'kuajing.pinduoduo.com',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9',
  'anti-content': '0aqWfqnygjKgjgT9l4JRLE3W262VxA-QTV1MlxhnYRn1A9D1mzjaz1ty1lOqk1OOi-nFbjn24B4DP_51wp1_EIPIkp8F-K4mzKvDH7bWNUsVIye5QV0w_OjLOsfN_aq9iiUWBRBn3TZZ2JWXuPzbCaoZUYuO8w3T-iiku5b3_SAT4iE6c62maxkI_opBRZTJ_TcKDRZTfRZDJ4GHIlHLtdnZHqg4pIBQKk3lKyRVBzLU439Z739384nmIP-Rg5oCBCPssp1p7T4NU4GGOgOog0oaqPXmYfFgBkV66j0_J9QeuGlTTdcOaoa4kjBNYNEdF26yWoO7kZ4wissi2ILOMdkJ-EkXOGWVWIzwmULFqsrDbCJRQ73JehgwSCdn2l19YaC_NciIZLxfjTiS0Ear_gUYOA-vWWnksZf8htqGFudzYKkdCwT-FxRG131qWjuJiDRhysaW0q_1as0uKOlMRUq5g3wFnq_tgS6u5J2aHhN_NLI87bMEJTkkjvnFJMS7W4O9wxM0tTbS3Np2moTxB623zU5X536QAWD_BZtT0SvIkINdJGmfwASrzYJAxJAY8-Ipl6D-s0XIlWNyDTwvJZwxPLjbgrP1RzFRoAfYZ1X6lbPlKXkQw6oybvaKRbiBpBnP3BaI9z_QUJTMR3vAmBSPeeCnbCOej3D_UsnpWspIISEDVOu8RznDe8RaQB8rhLWTeG9T7idnbpz_6QYrWyYYl7tLHMGYNFCr4phixZgFrPe',
  'cache-control': 'max-age=0',
  'content-type': 'application/json',
  'cookie': '_bee=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; _f77=6f8352db-3d3b-4d22-840b-a7ea88876cc2; _a42=4f526040-7d9d-4151-bcec-b86be9d48bf9; api_uid=CmlqNWRGQQUDawBThno0Ag==; _nano_fp=XpEJX5Xxnpmjn0d8nC_gtoIgd1lWrNnWYuYin1UJ; rckk=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; ru1k=6f8352db-3d3b-4d22-840b-a7ea88876cc2; ru2k=4f526040-7d9d-4151-bcec-b86be9d48bf9; SUB_PASS_ID=eyJ0IjoieExxZm5Ud2VIcTVUeStPQTlPa1ZkcENCa0J3UnlTTVplNjJhQUhqZm85UXNDbWVUZm1yckU0b3NBTUJrZ0IveSIsInYiOjEsInMiOjEwMDAwLCJ1Ijo5MDQ2ODAyNDAxMzI5fQ==',
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

func()


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