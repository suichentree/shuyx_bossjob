import requests

# 用户名密码认证
username = "18277877821"
password = "qwe18277877821"
iport = "127.0.0.1:38888"

# 此代理有账户密码验证
proxies = {
    "http": f"http://{username}:{password}@{iport}",
    "https": f"http://{username}:{password}@{iport}"
}
# 使用代理IP发送请求
response = requests.get("https://www.baidu.com", proxies=proxies)



