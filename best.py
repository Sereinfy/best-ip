import dns.message
import dns.query
import dns.rdatatype
from dns.edns import ECSOption

# 要解析的域名列表
domains = [
    "visa.com",
    "bestcf.top",
]

# 输出文件
output_file = "dns_results.txt"

# 指定 DNS 服务器
dns_server = "8.8.8.8"

# 自定义 ECS（客户端子网），示例：
# IPv4: "1.2.3.4/24"
# IPv6: "2400:3200::/32"
ecs_subnet = "211.138.177.0/21"


def resolve_with_ecs(domain, qtype, server, ecs_subnet):
    ip_set = set()
    try:
        # 构造查询报文
        query = dns.message.make_query(domain, qtype)

        # 添加 ECS
        net, prefixlen = ecs_subnet.split("/")
        prefixlen = int(prefixlen)
        ecs = ECSOption(address=net, srclen=prefixlen, scopelen=0)
        query.use_edns(options=[ecs])

        # 发送查询
        response = dns.query.udp(query, server, timeout=3)

        for ans in response.answer:
            for item in ans.items:
                if item.rdtype == dns.rdatatype.A or item.rdtype == dns.rdatatype.AAAA:
                    ip_set.add(item.to_text())
    except Exception:
        pass
    return ip_set


def main(domains, output_file, server, ecs_subnet):
    all_ips = set()
    for domain in domains:
        for qtype in ["A", "AAAA"]:
            all_ips |= resolve_with_ecs(domain, qtype, server, ecs_subnet)

    # 排序：IPv4 在前，IPv6 在后
    ipv4_list = sorted([ip for ip in all_ips if "." in ip])
    ipv6_list = sorted([ip for ip in all_ips if ":" in ip])

    with open(output_file, "w", encoding="utf-8") as f:
        for ip in ipv4_list + ipv6_list:
            print(ip)
            f.write(ip + "\n")


if __name__ == "__main__":
    main(domains, output_file, dns_server, ecs_subnet)
    print(f"\n解析结果已保存到 {output_file}")
