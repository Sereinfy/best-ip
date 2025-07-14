import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在，不存在则创建
if not os.path.exists('ip.txt'):
    open('ip.txt', 'w').close()  # 创建空文件
else:
    # 如果存在则清空内容
    open('ip.txt', 'w').close()

# 创建一个文件来存储IP地址
with open('ip.txt', 'a') as file:  # 使用追加模式写入
    for url in urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://www.wetest.vip/page/cloudflare/address_v4.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('tr')
        
        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            
            # 如果找到IP地址,则写入文件
            for ip in ip_matches:
                文件。write(ip + '\n')

print('IP地址已保存到ip.txt文件中。')
