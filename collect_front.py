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

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('front.txt'):
    os.remove('front.txt')

# 创建一个文件来存储IP地址
with open('front.txt', 'w') as file:
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
                # 查找该<tr>中的所有<td>元素
                tds = element.find_all('td')
                contains_mobile = any("联通" in td.get_text() for td in tds)

                # 如果<td>中包含“移动”，则查找IP地址
                if contains_mobile:
                    element_text = element.get_text()
                    ip_matches = re.findall(ip_pattern, element_text)
                    
                    # 如果找到IP地址，则写入文件
                    for ip in ip_matches:
                        file.write(ip + '\n')
        except requests.exceptions.RequestException as e:
            print(f"访问 {url} 时出错: {e}")

print('IP地址已保存到front.txt文件中。')
