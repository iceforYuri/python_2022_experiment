import requests
# 做测试用
url = "https://sz.fang.lianjia.com/loupan/pg3/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text[:1000])  # 只打印前1000字符，避免刷屏