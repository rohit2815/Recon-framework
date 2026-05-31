#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║   Automated Reconnaissance Framework v1.0    ║
║   With AI-Powered Analysis (Claude)          ║
╚══════════════════════════════════════════════╝

Usage:
    python recon.py <domain>
    python recon.py <domain> --no-ai
    python recon.py <domain> --no-subdomains

⚠️  Only run on systems you have written authorization to test.
"""

import sys
import os
import json
import datetime
import argparse

from modules.subdomains import enumerate_subdomains
from modules.portscan    import scan_ports
from modules.banner      import grab_all_banners
from modules.cve_lookup  import lookup_all_cves
from modules.ai_assistant import analyze_findings, interactive_chat


BANNER = r"""
 ____                          _____
|  _ \ ___  ___ ___  _ __    |  ___| __ __ _ _ __ ___   ___
| |_) / _ \/ __/ _ \| '_ \   | |_ | '__/ _` | '_ ` _ \ / _ \
|  _ <  __/ (_| (_) | | | |  |  _|| | | (_| | | | | | |  __/
|_| \_\___|\___\___/|_| |_|  |_|  |_|  \__,_|_| |_| |_|\___|

  Automated Reconnaissance Framework v1.0  |  AI-Powered
  ⚠️  Authorized use only
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Automated Recon Framework with AI Analysis"
    )
    parser.add_argument("domain", help="Target domain (e.g. example.com)")
    parser.add_argument("--no-ai",         action="store_true", help="Skip AI analysis")
    parser.add_argument("--no-subdomains", action="store_true", help="Skip subdomain enumeration")
    parser.add_argument("--no-banners",    action="store_true", help="Skip banner grabbing")
    parser.add_argument("--no-cve",        action="store_true", help="Skip CVE lookup")
    parser.add_argument("--no-chat",       action="store_true", help="Skip interactive AI chat")
    parser.add_argument("--serve",         action="store_true", help="Launch Flask server after scan")
    return parser.parse_args()


def save_results(scan_data, domain):
    os.makedirs("output", exist_ok=True)
    json_path = f"output/{domain}_data.json"
    with open(json_path, "w") as f:
        json.dump(scan_data, f, indent=2)
    print(f"[+] Data saved → {json_path}")
    return json_path


def main():
    print(BANNER)
    args = parse_args()
    domain = args.domain.strip().lstrip("https://").lstrip("http://").rstrip("/")

    print(f"[*] Target: {domain}")
    print(f"[*] Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    scan_data = {
        "domain": domain,
        "date": str(datetime.date.today()),
        "subdomains": [],
        "open_ports": [],
        "ai_summary": "",
    }

    # Stage 1: Subdomain enumeration
    if not args.no_subdomains:
        print("━" * 50)
        print("  STAGE 1 — Subdomain Enumeration")
        print("━" * 50)
        scan_data["subdomains"] = enumerate_subdomains(domain)
    else:
        print("[~] Skipping subdomain enumeration")

    # Stage 2: Port scanning
    print("\n" + "━" * 50)
    print("  STAGE 2 — Port Scanning")
    print("━" * 50)
    scan_data["open_ports"] = scan_ports(domain)

    # Stage 3: Banner grabbing
    if not args.no_banners and scan_data["open_ports"]:
        print("\n" + "━" * 50)
        print("  STAGE 3 — Banner Grabbing")
        print("━" * 50)
        scan_data["open_ports"] = grab_all_banners(domain, scan_data["open_ports"])

    # Stage 4: CVE lookup
    if not args.no_cve and scan_data["open_ports"]:
        print("\n" + "━" * 50)
        print("  STAGE 4 — CVE Lookup (NVD API)")
        print("━" * 50)
        scan_data["open_ports"] = lookup_all_cves(scan_data["open_ports"])

    # Stage 5: AI analysis
    if not args.no_ai:
        print("\n" + "━" * 50)
        print("  STAGE 5 — AI Risk Analysis (Claude)")
        print("━" * 50)
        print("[*] Sending findings to AI for analysis...")
        compact = json.dumps(scan_data, indent=2)
        scan_data["ai_summary"] = analyze_findings(compact)
        print("[+] AI analysis complete.")

    # Save results
    print("\n" + "━" * 50)
    save_results(scan_data, domain)

    # Count stats
    total_cves = sum(len(p.get("cves", [])) for p in scan_data["open_ports"])
    high_crit  = sum(
        1 for p in scan_data["open_ports"]
        for c in p.get("cves", [])
        if c.get("severity") in ["Critical", "High"]
    )

    print(f"""
╔══════════════════════════════╗
  ✅ Scan Complete
  Subdomains  : {len(scan_data['subdomains'])}
  Open Ports  : {len(scan_data['open_ports'])}
  CVEs Found  : {total_cves}
  High/Crit   : {high_crit}
╚══════════════════════════════╝
  📄 View report: python app.py
     Then open: http://127.0.0.1:5000/report/{domain}
""")

    # Stage 6: Interactive AI chat
    if not args.no_ai and not args.no_chat:
        sys.stdout.flush()
        sys.stderr.flush()
        interactive_chat(json.dumps(scan_data, indent=2))

    # Launch Flask server
    if args.serve:
        import subprocess
        subprocess.run([sys.executable, "app.py"])


if __name__ == "__main__":
    main()
