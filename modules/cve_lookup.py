import requests
import time


NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def get_cvss_severity(score):
    """Return severity label from CVSS score."""
    if score is None:
        return "Unknown"
    score = float(score)
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    else:
        return "Low"


def get_cves(product, version="", max_results=5):
    """Fetch CVEs from the NVD API for a given product/version."""
    if not product or product == "unknown":
        return []

    query = f"{product} {version}".strip()
    params = {
        "keywordSearch": query,
        "resultsPerPage": max_results,
    }

    try:
        res = requests.get(NVD_API, params=params, timeout=10)
        if res.status_code != 200:
            return []

        data = res.json()
        cves = []

        for item in data.get("vulnerabilities", []):
            cve = item.get("cve", {})
            cve_id = cve.get("id", "")
            descriptions = cve.get("descriptions", [])
            desc = next(
                (d["value"] for d in descriptions if d["lang"] == "en"),
                "No description available.",
            )

            # Extract CVSS score
            cvss_score = None
            metrics = cve.get("metrics", {})
            for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                if key in metrics:
                    try:
                        cvss_score = metrics[key][0]["cvssData"]["baseScore"]
                    except (KeyError, IndexError):
                        pass
                    break

            cves.append({
                "id": cve_id,
                "description": desc[:300],
                "cvss_score": cvss_score,
                "severity": get_cvss_severity(cvss_score),
                "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
            })

        time.sleep(0.6)  # NVD rate limit: 5 req/30s without API key
        return cves

    except Exception as e:
        print(f"[!] CVE lookup error for '{query}': {e}")
        return []


def lookup_all_cves(open_ports):
    """Look up CVEs for all services found in port scan."""
    print("[*] Looking up CVEs for discovered services...")
    for port_info in open_ports:
        product = port_info.get("product") or port_info.get("service", "")
        version = port_info.get("version", "")
        if product and product != "unknown":
            cves = get_cves(product, version)
            port_info["cves"] = cves
            if cves:
                print(f"  [+] Port {port_info['port']} ({product}): {len(cves)} CVEs found")
        else:
            port_info["cves"] = []
    return open_ports
