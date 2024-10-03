import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://www.wetest.vip/page/cloudfront/ipv4.html',
    'https://api.uouin.com/cloudflare.html',
    'https://ipdb.030101.xyz/bestcf/'
]

# 自定义正则表达式用于智能匹配IP地址
ip_pattern = r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

# 检查front.txt文件是否存在，如果存在则删除它
if os.path.exists('front.txt'):
    os.remove('front.txt')

# 创建一个集合来存储IP地址，避免重复
unique_ips = set()

# 初始化一个Session对象
session = requests.Session()
# 设置请求头，模拟浏览器访问
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
})

# 创建一个文件来存储IP地址
with open('front.txt', 'w') as file:
    for url in urls:
        try:
            # 使用Session对象发送HTTP请求获取网页内容
            response = session.get(url, timeout=10)  # 设置超时参数
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取纯文本内容
            text = soup.get_text()

            # 查找页面中的IP地址
            ip_matches = re.findall(ip_pattern, text)

            # 遍历所有匹配的IP地址
            for ip in ip_matches:
                if ip not in unique_ips:
                    unique_ips.add(ip)
                    file.write(ip + '\n')
        except requests.RequestException as e:
            print(f"请求{url}时出错: {e}")

print('IP地址已保存到front.txt文件中。')
