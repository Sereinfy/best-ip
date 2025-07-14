import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

# 用户代理头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 目标URL列表（需要JS处理的URL）
JS_URLS = [
    'https://ipdb.030101.xyz/bestcfv4/',
    'https://api.uouin.com/cloudflare.html'  # 需要等待1秒刷新
]

# 普通URL列表
NORMAL_URLS = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
    'https://ip.164746.xyz'
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

def init_selenium():
    """初始化Selenium（适配GitHub Actions）"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # GitHub Actions 需要指定Chrome二进制路径
    options.binary_location = '/usr/bin/google-chrome'
    
    # 自动下载并配置ChromeDriver
    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_with_selenium(url):
    """使用Selenium爬取JS动态刷新的页面"""
    print(f"正在使用Selenium爬取动态页面: {url}")
    try:
        driver = init_selenium()
        driver.get(url)
        
        # 针对 api.uouin.com 等待1秒刷新数据
        if 'api.uouin.com' in url:
            time.sleep(3)  # 稍微多等0.5秒确保稳定
        
        page_source = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(page_source, 'html.parser')
        ips = extract_ips_from_tr(soup)
        if not ips:
            ips = extract_ips(page_source)
        return ips
    except Exception as e:
        print(f"错误: Selenium爬取 {url} 失败 - {str(e)}")
        return []

def scrape_normal_url(url):
    """爬取普通静态页面"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        ips = extract_ips_from_tr(soup)
        if not ips:
            ips = extract_ips(response.text)
        return ips
    except Exception as e:
        print(f"错误: 爬取 {url} 失败 - {str(e)}")
        return []

def main():
    # 爬取普通URL
    for url in NORMAL_URLS:
        print(f"\n正在爬取普通页面: {url}")
        ips = scrape_normal_url(url)
        if not ips:
            print(f"⚠️ 警告: 从 {url} 中未找到IP地址")
        else:
            print(f"✅ 找到 {len(ips)} 个IP:")
            for ip in ips:
                print(f"  - {ip}")
            all_ips.extend(ips)
    
    # 爬取JS动态URL
    for url in JS_URLS:
        print(f"\n正在爬取动态页面: {url}")
        ips = scrape_with_selenium(url)
        if not ips:
            print(f"⚠️ 警告: 从 {url} 中未找到IP地址")
        else:
            print(f"✅ 找到 {len(ips)} 个IP:")
            for ip in ips:
                print(f"  - {ip}")
            all_ips.extend(ips)
    
    # 去重并保存
    unique_ips = list(set(all_ips))
    with open('ip.txt', 'w') as f:
        for ip in unique_ips:
            f.write(ip + '\n')
    
    print(f"\n✅ 完成! 共找到 {len(unique_ips)} 个唯一IP地址，已保存到 ip.txt")

if __name__ == '__main__':
    main()
