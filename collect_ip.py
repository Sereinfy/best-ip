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
    'https://ipdb.030101.xyz/bestcfv4/'
]

# 存储所有找到的IP地址
all_ips = []

def extract_ips_from_tr(soup):
    """从<tr>标签中提取IP地址"""
    ips = []
    for tr in soup.find_all('tr'):
        text = tr.get_text()
        # 提取IP地址
        ip_matches = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
        if ip_matches:
            ips.extend(ip_matches)
    return ips

def scrape_url(url):
    """爬取单个URL并提取IP地址"""
    try:
        print(f"正在爬取: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 方法1：优先从<tr>标签中提取
        ips = extract_ips_from_tr(soup)
        
        # 方法2：如果没找到，再从整个页面文本中提取（备用方法）
        if not ips:
            print("从<tr>标签中未找到IP，尝试从整个页面提取...")
            text = soup.get_text()
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
        
        if not ips:
            print(f"警告: 从 {url} 中未找到IP地址")
        else:
            print(f"从 {url} 中找到 {len(ips)} 个IP地址")
            all_ips.extend(ips)
            
    except requests.exceptions.RequestException as e:
        print(f"错误: 爬取 {url} 失败 - {str(e)}")
    except Exception as e:
        print(f"错误: 处理 {url} 时发生意外错误 - {str(e)}")

# 遍历所有URL进行爬取
for url in urls:
    scrape_url(url)

# 去重
unique_ips = list(set(all_ips))

# 保存到文件
with open('ip.txt', 'w') as f:
    for ip in unique_ips:
        f.write(ip + '\n')

print(f"\n完成! 共找到 {len(unique_ips)} 个唯一IP地址，已保存到 ip.txt")
