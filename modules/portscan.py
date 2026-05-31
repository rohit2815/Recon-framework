import nmap


def scan_ports(target):
    """Scan top 1000 ports with service/version detection."""
    print(f"[*] Scanning ports on {target}...")
    nm = nmap.PortScanner()

    try:
        nm.scan(target, arguments="-sV -T4 --top-ports 1000 --open")
    except Exception as e:
        print(f"[!] Nmap error: {e}")
        return []

    results = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                port_info = nm[host][proto][port]
                if port_info["state"] == "open":
                    results.append({
                        "port": port,
                        "protocol": proto,
                        "state": port_info["state"],
                        "service": port_info.get("name", "unknown"),
                        "version": port_info.get("version", ""),
                        "product": port_info.get("product", ""),
                        "extrainfo": port_info.get("extrainfo", ""),
                    })

    print(f"[+] Found {len(results)} open ports on {target}")
    return results
