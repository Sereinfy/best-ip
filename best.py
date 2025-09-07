import dns.resolver

# 要解析的域名列表
domains = [
    "visa.com",
    "bestcf.top",
]

# 指定 DNS 服务器（可改成自己需要的，比如 8.8.8.8, 1.1.1.1, 9.9.9.9）
resolver = dns.resolver.Resolver()
resolver.nameservers = ["211.138.180.2"]

output_file = "dns_best_ip.txt"

def resolve_domains(domains, output_file):
    ip_set = set()  # 用于去重

    for domain in domains:
        for qtype in ["A", "AAAA"]:  # A=IPv4, AAAA=IPv6
            try:
                answers = resolver.resolve(domain, qtype)
                for rdata in answers:
                    ip_set.add(rdata.to_text())
            except Exception:
                pass  # 忽略解析失败

    # 排序：IPv4 在前，IPv6 在后
    ipv4_list = sorted([ip for ip in ip_set if "." in ip])
    ipv6_list = sorted([ip for ip in ip_set if ":" in ip])

    with open(output_file, "w", encoding="utf-8") as f:
        for ip in ipv4_list + ipv6_list:
            print(ip)
            f.write(ip + "\n")

if __name__ == "__main__":
    resolve_domains(domains, output_file)
    print(f"\n解析结果已保存到 {output_file}")
