# 🔍 Automated Reconnaissance Framework v1.0

> AI-powered recon pipeline — subdomain enumeration, port scanning, banner grabbing, CVE lookup, and Claude AI analysis — all in one tool.

⚠️ **Only use on systems you have explicit written authorization to test.**

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Nmap must also be installed on your system:
> - Linux: `sudo apt install nmap`
> - macOS: `brew install nmap`
> - Windows: Download from https://nmap.org/download.html

### 2. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Get a free API key at: https://console.anthropic.com

### 3. Run the framework

```bash
python recon.py testfire.net
```

### 4. View the report

```bash
python app.py
# Open: http://127.0.0.1:5000/report/testfire.net
```

---

## 📁 Project Structure

```
recon-framework/
├── recon.py              # Main orchestrator — run this
├── app.py                # Flask server for viewing reports
├── modules/
│   ├── subdomains.py     # Subdomain enumeration (crt.sh + DNS brute-force)
│   ├── portscan.py       # Nmap port scanner (top 1000 ports + service detection)
│   ├── banner.py         # Banner grabbing (HTTP headers + raw socket)
│   ├── cve_lookup.py     # CVE lookup via NVD API with CVSS scoring
│   └── ai_assistant.py   # Claude AI analysis + interactive chat
├── templates/
│   └── report.html       # Dark-themed HTML report with AI chat UI
├── output/               # Generated reports saved here
└── requirements.txt
```

---

## 🎮 Usage Options

```bash
# Full scan (all stages + AI analysis + interactive chat)
python recon.py example.com

# Skip AI (faster, no API key needed)
python recon.py example.com --no-ai

# Skip subdomain enumeration
python recon.py example.com --no-subdomains

# Skip CVE lookup
python recon.py example.com --no-cve

# Scan and immediately launch the web server
python recon.py example.com --serve

# All options
python recon.py --help
```

---

## 🧪 Legal Testing Targets

| Target | Notes |
|--------|-------|
| `scanme.nmap.org` | Nmap's official test host — always legal |
| `localhost` / your own VPS | Full control |
| HackTheBox / TryHackMe VMs | Lab environments with permission |
| DVWA (Docker) | `docker run -p 80:80 vulnerables/web-dvwa` |

---

## 🤖 AI Assistant Features

- **Auto-analysis** after every scan — risk score, top findings, attack surface
- **Interactive CLI chat** — ask questions about the scan results
- **In-report chat UI** — ask the AI directly from the HTML report in your browser

---

## 📝 Resume Description

> *"Built an AI-powered Python reconnaissance framework integrating subdomain enumeration (crt.sh + DNS brute-force), Nmap port scanning, banner grabbing, and NVD CVE lookup (CVSS scoring) into a single automated pipeline. Embedded a Claude AI assistant that auto-analyzes findings, explains vulnerabilities in plain English, and supports interactive Q&A via a Flask-served dark-themed HTML report. Tested legally on HackTheBox, TryHackMe, and scanme.nmap.org."*

**ATS Keywords:** Python, Nmap, OSINT, Reconnaissance, CVE Analysis, NVD API, CVSS, Flask, Jinja2, Subdomain Enumeration, AI Security Tools, Vulnerability Assessment, Penetration Testing

---

## 🔧 Troubleshooting

**Nmap permission error (port scan returns nothing):**
```bash
sudo python recon.py example.com
```

**NVD API rate limit (HTTP 403/429):**
Get a free NVD API key at https://nvd.nist.gov/developers/request-an-api-key and add to `cve_lookup.py`:
```python
headers = {"apiKey": "YOUR_NVD_API_KEY"}
res = requests.get(NVD_API, params=params, headers=headers, timeout=10)
```

**AI errors:**
Make sure `ANTHROPIC_API_KEY` is set in your environment.
