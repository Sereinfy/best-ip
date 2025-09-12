import dns.message
import dns.query
import dns.rdatatype
from dns.edns import ECSOption

# ===== 配置部分 =====

ecs_list = [
    "211.138.177.0/21",
    "61.132.163.0/24",
    "211.91.88.0/24"
]

domain_ecs_map = {
    "visa.com": ecs_list,
    "bestcf.top": ecs_list,
    "canva.com": ecs_list,
    "cnamefuckxxs.yuchen.icu": ecs_list,
    "cfip.xxxxxxxx.tk": ["211.138.177.0/21"],
    "cf.0sm.com": ["211.138.177.0/21"],
}

output_file = "dns_best_ip.txt"
detailed_file = "dns_results.txt"

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

        try:
            response = dns.query.udp(query, server, timeout=5)
        except Exception:
            response = dns.query.tcp(query, server, timeout=5)

        for ans in response.answer:
            for item in ans.items:
                if item.rdtype == dns.rdatatype.A:  # 只收集 IPv4
                    ip_list.append(item.to_text())
    except Exception as e:
        print(f"[ERROR] {domain} {qtype} with ECS {ecs_subnet} 查询失败: {e}")
    return ip_list


def main():
    all_ips = []
    detailed_results = []

    for domain, ecs_subnets in domain_ecs_map.items():
        for ecs_subnet in ecs_subnets:
            print(f"\n🔍 使用 ECS {ecs_subnet} 解析 {domain} ...")
            ips = resolve_with_ecs(domain, "A", dns_server, ecs_subnet)
            for ip in ips:
                all_ips.append(ip)
                detailed_results.append((domain, ecs_subnet, ip))

    # 去重 IP
    unique_ips = list(dict.fromkeys(all_ips))
    with open(output_file, "w", encoding="utf-8") as f:
        for ip in unique_ips:
            print(ip)
            f.write(ip + "\n")

    # 按域名分块并去重 domain+ECS+IP
    from collections import defaultdict, OrderedDict

    domain_dict = defaultdict(list)
    seen = set()
    for domain, ecs, ip in detailed_results:
        key = (domain, ecs, ip)
        if key not in seen:
            seen.add(key)
            domain_dict[domain].append((ecs, ip))

    # 保持域名顺序
    ordered_domain_dict = OrderedDict()
    for domain in domain_ecs_map.keys():
        if domain in domain_dict:
            ordered_domain_dict[domain] = domain_dict[domain]

    # 写详细结果
    with open(detailed_file, "w", encoding="utf-8") as f:
        for domain, ecs_list in ordered_domain_dict.items():
            f.write(f"{domain}:\n")
            for ecs, ip in ecs_list:
                f.write(f"  [{ecs}] {ip}\n")
            f.write("\n")

    print(f"\n✅ 解析完成，结果已保存到 {output_file} 和 {detailed_file}")


if __name__ == "__main__":
    main()
