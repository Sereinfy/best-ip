import requests
from bs4 import BeautifulSoup
import re
import time  # 添加这行导入

# 配置部分
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
TARGETS = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
    'https://ip.164746.xyz',
    'https://api.uouin.com/cloudflare.html'  # 注意：该站点有1秒延迟刷新
]

def extract_ips(text):
    """使用正则提取所有IPv4地址"""
    return re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)

def scrape_site(url):
    """核心爬取逻辑"""
    try:
        print(f"\n🔍 正在爬取: {url}")
        
        # 特殊处理api.uouin的延迟加载
        delay = 1.5 if 'api.uouin.com' in url else 0
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        if delay:
            print(f"⏳ 等待 {delay}秒让数据刷新...")
            time.sleep(delay)
            # 需要二次请求获取最新数据
            response = requests.get(url, headers=HEADERS, timeout=10)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 优先从表格行提取
        ips = []
        for tr in soup.find_all('tr'):
            ips.extend(extract_ips(tr.get_text()))
        
        # 备用方案：全局搜索
        if not ips:
            ips = extract_ips(response.text)
            
        return list(set(ips))  # 立即去重
    
    except Exception as e:
        print(f"❌ 爬取失败: {str(e)}")
        return []

if __name__ == '__main__':
    all_ips = []
    
    for target in TARGETS:
        if result := scrape_site(target):
            print(f"✅ 发现 {len(result)} 个IP:")
            print("\n".join(f"  - {ip}" for ip in result))
            all_ips.extend(result)
    
    # 最终去重保存
    with open('ip.txt', 'w') as f:
        f.write("\n".join(sorted(set(all_ips))))
    
    print(f"\n🎉 完成！共收集 {len(set(all_ips))} 个唯一IP")
