import requests
from bs4 import BeautifulSoup
import re
import time

# 配置部分
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 主要目标网址（结果保存到ip.txt）
MAIN_TARGETS = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
    'https://ip.164746.xyz',
    'https://api.uouin.com/cloudflare.html'
]

# 特殊目标网址（结果单独保存到front.txt）
SPECIAL_TARGET = 'https://www.wetest.vip/page/cloudfront/ipv4.html'

def extract_ips(text):
    """使用正则提取所有IPv4地址"""
    return re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)

def scrape_site(url, delay_seconds=10):
    """核心爬取逻辑"""
    try:
        print(f"\n🔍 正在爬取: {url}")
        
        # 首次请求
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        # 等待指定时间
        if delay_seconds > 0:
            print(f"⏳ 等待 {delay_seconds}秒...")
            time.sleep(delay_seconds)
            # 二次请求获取最新数据
            response = requests.get(url, headers=HEADERS, timeout=15)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 优先从表格行提取
        ips = []
        for tr in soup.find_all('tr'):
            ips.extend(extract_ips(tr.get_text()))
        
        # 备用方案：全局搜索
        if not ips:
            ips = extract_ips(response.text)
            
        return list(set(ips))  # 去重后返回
    
    except Exception as e:
        print(f"❌ 爬取失败: {str(e)}")
        return []

if __name__ == '__main__':
    # 爬取主要目标
    main_ips = []
    for target in MAIN_TARGETS:
        if result := scrape_site(target):
            print(f"✅ 发现 {len(result)} 个IP:")
            print("\n".join(f"  - {ip}" for ip in result))
            main_ips.extend(result)
    
    # 爬取特殊目标
    print(f"\n🌟 开始处理特殊目标: {SPECIAL_TARGET}")
    front_ips = scrape_site(SPECIAL_TARGET)
    
    # 保存结果
    with open('ip.txt', 'w') as f:
        f.write("\n".join(sorted(set(main_ips))))
    
    with open('front.txt', 'w') as f:
        f.write("\n".join(sorted(set(front_ips))))
    
    print(f"\n🎉 完成！")
    print(f"主IP列表: {len(set(main_ips))} 个（已保存到ip.txt）")
    print(f"CloudFront IP列表: {len(set(front_ips))} 个（已保存到front.txt）")
