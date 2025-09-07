import dns.message
import dns.query
import dns.rdatatype
from dns.edns import ECSOption

# ===== 配置部分 =====

# 要解析的域名列表
domains = [
    "visa.com",
    "bestcf.top",
]

# 输出文件
output_file = "dns_best_ip.txt"

# DNS 服务器
dns_server = "8.8.8.8"

# 多个 ECS 列表，直接写在代码里
ecs_list = [
    "211.138.177.0/21",
    "61.132.163.68/24",
    "211.91.88.129/24"
]

# ===================


def resolve_with_ecs(domain, qtype, server, ecs_subnet):
    ip_set = set()
    try:
        query = dns.message.make_query(domain, qtype)

        net, prefixlen = ecs_subnet.strip().split("/")
        prefixlen = int(prefixlen)
        ecs = ECSOption(address=net, srclen=prefixlen, scopelen=0)
        query.use_edns(options=[ecs])

        # 用 TCP，避免 CI UDP 丢包
        response = dns.query.tcp(query, server, timeout=5)

        for ans in response.answer:
            for item in ans.items:
                if item.rdtype in (dns.rdatatype.A, dns.rdatatype.AAAA):
                    ip_set.add(item.to_text())
    except Exception as e:
        print(f"[ERROR] {domain} {qtype} with ECS {ecs_subnet} 查询失败: {e}")
    return ip_set


def main():
    all_ips = set()

    for ecs_subnet in ecs_list:
        ecs_subnet = ecs_subnet.strip()
        if not ecs_subnet:
            continue
        print(f"\n🔍 使用 ECS {ecs_subnet} 进行解析...")
        for domain in domains:
            for qtype in ["A", "AAAA"]:
                all_ips |= resolve_with_ecs(domain, qtype, dns_server, ecs_subnet)

    # 去重 + 排序
    ipv4_list = sorted([ip for ip in all_ips if "." in ip])
    ipv6_list = sorted([ip for ip in all_ips if ":" in ip])

    with open(output_file, "w", encoding="utf-8") as f:
        for ip in ipv4_list + ipv6_list:
            print(ip)
            f.write(ip + "\n")

    print(f"\n✅ 解析完成，结果已保存到 {output_file}")


if __name__ == "__main__":
    main()
