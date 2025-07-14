import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# 用户代理头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Cloudflare 相关URL
CLOUDFLARE_URLS = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
    'https://ip.164746.xyz'
]

# CloudFront 相关URL
CLOUDFRONT_URL = 'https://www.wetest.vip/page/cloudfront/ipv4.html'

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

def scrape_cloudflare_ips():
    """专门爬取Cloudflare IP"""
    cloudflare_ips = []
    for url in CLOUDFLARE_URLS:
        try:
            print(f"\n正在爬取Cloudflare IP: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            ips = extract_ips_from_tr(soup)
            if not ips:
                ips = extract_ips(response.text)
            
            if not ips:
                print(f"⚠️ 警告: 从 {url} 中未找到IP地址")
            else:
                print(f"✅ 找到 {len(ips)} 个Cloudflare IP:")
                for ip in ips:
                    print(f"  - {ip}")
                cloudflare_ips.extend(ips)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 错误: 爬取 {url} 失败 - {str(e)}")
        except Exception as e:
            print(f"❌ 错误: 处理 {url} 时发生意外错误 - {str(e)}")
    
    return list(set(cloudflare_ips))  # 返回去重后的IP列表

def scrape_cloudfront_ips():
    """专门爬取CloudFront IP"""
    try:
        print(f"\n正在爬取CloudFront IP: {CLOUDFRONT_URL}")
        response = requests.get(CLOUDFRONT_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        ips = extract_ips_from_tr(soup)
        if not ips:
            ips = extract_ips(response.text)
        
        if not ips:
            print(f"⚠️ 警告: 从 {CLOUDFRONT_URL} 中未找到IP地址")
            return []
        else:
            print(f"✅ 找到 {len(ips)} 个CloudFront IP:")
            for ip in ips:
                print(f"  - {ip}")
            return list(set(ips))  # 返回去重后的IP列表
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 错误: 爬取 {CLOUDFRONT_URL} 失败 - {str(e)}")
        return []
    except Exception as e:
        print(f"❌ 错误: 处理 {CLOUDFRONT_URL} 时发生意外错误 - {str(e)}")
        return []

def save_ips_to_file(ips, filename):
    """将IP列表保存到文件"""
    with open(filename, 'w') as f:
        for ip in ips:
            f.write(ip + '\n')
    print(f"已保存 {len(ips)} 个IP到 {filename}")

def main():
    # 爬取并保存Cloudflare IP
    cloudflare_ips = scrape_cloudflare_ips()
    save_ips_to_file(cloudflare_ips, 'ip.txt')
    
    # 爬取并保存CloudFront IP
    cloudfront_ips = scrape_cloudfront_ips()
    save_ips_to_file(cloudfront_ips, 'front.txt')
    
    print("\n✅ 所有任务完成!")

if __name__ == '__main__':
    main()
