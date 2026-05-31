import requests
import dns.resolver


def enumerate_subdomains(domain):
    """Enumerate subdomains using crt.sh certificate transparency logs."""
    subs = set()

    # Method 1: crt.sh API
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            for entry in res.json():
                name = entry.get("name_value", "")
                for s in name.split("\n"):
                    s = s.strip().lstrip("*.")
                    if domain in s and s != domain:
                        subs.add(s)
    except Exception as e:
        print(f"[!] crt.sh error: {e}")

    # Method 2: DNS brute-force with common prefixes
    common_prefixes = [
        "www", "mail", "ftp", "admin", "api", "dev", "staging",
        "test", "portal", "vpn", "remote", "blog", "shop", "cdn",
        "app", "dashboard", "secure", "login", "webmail"
    ]
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2

    for prefix in common_prefixes:
        subdomain = f"{prefix}.{domain}"
        try:
            resolver.resolve(subdomain, "A")
            subs.add(subdomain)
        except Exception:
            pass

    result = list(subs)
    print(f"[+] Found {len(result)} subdomains for {domain}")
    return result
