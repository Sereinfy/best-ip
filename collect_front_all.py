import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://www.wetest.vip/page/cloudfront/ipv4.html'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

# 检查front.txt文件是否存在，如果不存在则创建
if not os.path.exists('front.txt'):
    open('front.txt', 'w').close()  # 创建空文件

# 清空文件内容（如果已有内容）
with open('front.txt', 'w') as file:
    pass  # 只是打开并立即关闭，清空文件

# 写入IP地址到文件
with open('front.txt', 'a') as file:  # 使用追加模式
    for url in urls:
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url, timeout=10)
            # 检查响应状态码是否为200
            if response.status_code != 200:
                print(f"无法访问 {url}，状态码: {response.status_code}")
                continue
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 找到所有<tr>元素
            elements = soup.find_all('tr')
            
            # 遍历所有<tr>元素
            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)
                
                # 如果找到IP地址，则写入文件
                for ip in ip_matches:
                    file.write(ip + '\n')
        except requests.exceptions.RequestException as e:
            print(f"访问 {url} 时出错: {e}")

print('IP地址已保存到front.txt文件中。')
