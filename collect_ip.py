import requests
from bs4 import BeautifulSoup
import re

# 用户代理头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 定义URL组
url_groups = {
    'cloudflare': [
        'https://www.wetest.vip/page/cloudflare/address_v4.html',
        'https://ip.164746.xyz'
    ],
    'cloudfront': [
        'https://www.wetest.vip/page/cloudfront/ipv4.html'
    ]
}

def extract_ips(text):
    """通用IP提取函数"""
    return re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)

def extract_ips_from_tr(soup):
    """从表格行提取IP"""
    ips = []
    for tr in soup.find_all('tr'):
        ips.extend(extract_ips(tr.get_text()))
    return ips

def scrape_ips(urls):
    """通用爬取函数"""
    results = []
    for url in urls:
        try:
            print(f"\n正在爬取: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            ips = extract_ips_from_tr(soup) or extract_ips(response.text)
            
            if not ips:
                print(f"⚠️ 未找到IP: {url}")
                continue
                
            print(f"✅ 找到 {len(ips)} 个IP")
            results.extend(ips)
            
        except Exception as e:
            print(f"❌ 爬取失败: {url} - {str(e)}")
    
    return list(set(results))  # 去重

def save_ips(ips, filename):
    """保存IP到文件"""
    with open(filename, 'w') as f:
        f.write('\n'.join(ips))
    print(f"已保存 {len(ips)} 个IP到 {filename}")

def main():
    # 爬取并保存Cloudflare IP
    cf_ips = scrape_ips(url_groups['cloudflare'])
    save_ips(cf_ips, 'ip.txt')
    
    # 爬取并保存CloudFront IP
    front_ips = scrape_ips(url_groups['cloudfront'])
    save_ips(front_ips, 'front.txt')
    
    print("\n✅ 所有任务完成！")

if __name__ == '__main__':
    main()
