import socket
import requests


def grab_banner(ip, port, timeout=3):
    """Grab banner from a specific port."""
    banner = ""

    # HTTP/HTTPS banner via requests
    if port in [80, 443, 8080, 8443, 8000]:
        protocol = "https" if port in [443, 8443] else "http"
        try:
            res = requests.get(
                f"{protocol}://{ip}:{port}",
                timeout=timeout,
                allow_redirects=True,
                verify=False,
            )
            server = res.headers.get("Server", "")
            powered = res.headers.get("X-Powered-By", "")
            banner = f"{server} {powered}".strip()
        except Exception:
            pass
    else:
        # Raw socket banner grab
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((ip, port))
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            raw = s.recv(1024).decode("utf-8", errors="ignore")
            banner = raw.split("\n")[0].strip()
            s.close()
        except Exception:
            pass

    return banner


def grab_all_banners(target, open_ports):
    """Grab banners for all open ports."""
    print(f"[*] Grabbing banners on {target}...")
    for port_info in open_ports:
        banner = grab_banner(target, port_info["port"])
        port_info["banner"] = banner
        if banner:
            print(f"  [+] Port {port_info['port']}: {banner[:60]}")
    return open_ports
