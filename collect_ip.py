import requests
from bs4 import BeautifulSoup
import re

# 用户代理头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 目标URL列表
urls = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
    'https://ip.164746.xyz',
    'https://api.uouin.com/cloudflare.html',
    'https://ipdb.030101.xyz/bestcfv4/'  # 修正后的URL
]

# 存储所有找到的IP地址
all_ips = []

def extract_ips(text):
    """从文本中提取IPv4地址"""
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.findall(ip_pattern, text)

def extract_ips_from_tr(soup):
    """从<tr>标签中提取IP地址"""
    ips = []
    for tr in soup.find_all('tr'):
        text = tr.get_text()
        ip_matches = extract_ips(text)
        if ip_matches:
            ips.extend(ip_matches)
    return ips

def scrape_url(url):
    """爬取单个URL并提取IP地址"""
    try:
        print(f"\n正在爬取: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        soup = BeautifulSoup(response.text, 'html.parser')
        ips = extract_ips_from_tr(soup)
        if not ips:  # 如果<tr>里没有，再从整个页面提取
            ips = extract_ips(response.text)
        
        if not ips:
            print(f"⚠️ 警告: 从 {url} 中未找到IP地址")
        else:
            print(f"✅ 找到 {len(ips)} 个IP:")
            for ip in ips:
                print(f"  - {ip}")
            all_ips.extend(ips)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 错误: 爬取 {url} 失败 - {str(e)}")
    except Exception as e:
        print(f"❌ 错误: 处理 {url} 时发生意外错误 - {str(e)}")

# 遍历所有URL进行爬取
for url in urls:
    scrape_url(url)

# 去重
unique_ips = list(set(all_ips))

# 保存到文件
with open('ip.txt', 'w') as f:
    for ip in unique_ips:
        f.write(ip + '\n')

print(f"\n✅ 完成! 共找到 {len(unique_ips)} 个唯一IP地址，已保存到 ip.txt")
