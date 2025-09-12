import dns.message 
import dns.query 
import dns.rdatatype 
from dns.edns import ECSOption 

# ===== 配置部分 ===== 

# 统一配置：域名 -> 需要使用的 ECS 列表 
# 如果要用全部 ECS，就写 ecs_list 
ecs_list = [ 
    "211.138.177.0/21", 
    "61.132.163.68/24", 
    "211.91.88.129/24" 
] 

domain_ecs_map = { 
    "visa.com": ecs_list,  
    "bestcf.top": ecs_list, 
    "canva.com": ecs_list,  
    "cnamefuckxxs.yuchen.icu": ecs_list, 
    "cfip.xxxxxxxx.tk": ["211.138.177.0/21"], 
    "cf.0sm.com": ["211.138.177.0/21"], 
} 

# 输出文件 
output_file = "dns_best_ip.txt" 

# DNS 服务器 
dns_server = "8.8.8.8" 

# =================== 

def resolve_with_ecs(domain, qtype, server, ecs_subnet): 
    ip_list = [] 
    try: 
        query = dns.message.make_query(domain, qtype) 

        net, prefixlen = ecs_subnet.strip().split("/") 
        prefixlen = int(prefixlen) 
        ecs = ECSOption(address=net, srclen=prefixlen, scopelen=0) 
        query.use_edns(options=[ecs]) 

        response = dns.query.tcp(query, server, timeout=5) 

        for ans in response.answer: 
            for item in ans.items: 
                if item.rdtype in (dns.rdatatype.A, dns.rdatatype.AAAA): 
                    ip_list.append(item.to_text()) 
    except Exception as e: 
        print(f"[ERROR] {domain} {qtype} with ECS {ecs_subnet} 查询失败: {e}") 
    return ip_list 

def main(): 
    all_ips = [] 
    domain_ip_map = {}  # 保存域名对应 IP

    for domain, ecs_subnets in domain_ecs_map.items(): 
        for ecs_subnet in ecs_subnets: 
            print(f"\n🔍 使用 ECS {ecs_subnet} 解析 {domain} ...") 
            for qtype in ["A"]: 
                ips = resolve_with_ecs(domain, qtype, dns_server, ecs_subnet) 
                all_ips.extend(ips)
                
                # 保存域名对应关系
                if domain not in domain_ip_map:
                    domain_ip_map[domain] = []
                domain_ip_map[domain].extend(ips)

    # 去重但保持顺序
    unique_ips = list(dict.fromkeys(all_ips)) 

    # 写入 dns_best_ip.txt
    with open(output_file, "w", encoding="utf-8") as f: 
        for ip in unique_ips: 
            print(ip) 
            f.write(ip + "\n") 

    # 写入域名-IP对应关系文件 dns_results.txt
    domain_ip_file = "dns_results.txt"
    with open(domain_ip_file, "w", encoding="utf-8") as f:
        for domain, ips in domain_ip_map.items():
            f.write(f"{domain}:\n")  # 域名加冒号
            # 去重 IP 并保持顺序
            unique_domain_ips = list(dict.fromkeys(ips))
            for ip in unique_domain_ips:
                f.write(f"  {ip}\n")  # IP 缩进两个空格

    print(f"\n✅ 解析完成，结果已保存到 {output_file} 和 {domain_ip_file}")

if __name__ == "__main__": 
    main()
