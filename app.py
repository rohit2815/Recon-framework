from flask import Flask, request, jsonify, render_template
from modules.ai_assistant import ask_ai
import os, json, glob

app = Flask(__name__)


@app.route("/")
def index():
    """List all generated reports."""
    reports = glob.glob("output/*.json")
    domains = [os.path.basename(r).replace("_data.json", "") for r in reports]
    links = "".join(f'<li><a href="/report/{d}">{d}</a></li>' for d in domains)
    return f"""
    <html><head><title>Recon Reports</title>
    <style>body{{font-family:monospace;background:#0d1117;color:#e6edf3;padding:40px}}
    a{{color:#58a6ff}} li{{margin:8px 0}}</style></head>
    <body><h2>🔍 Recon Reports</h2>
    <ul>{links if links else "<li>No reports yet. Run recon.py first.</li>"}</ul>
    </body></html>
    """


@app.route("/report/<domain>")
def report(domain):
    """Serve the HTML report for a domain."""
    data_file = f"output/{domain}_data.json"
    if not os.path.exists(data_file):
        return f"Report for {domain} not found. Run recon.py first.", 404

    with open(data_file) as f:
        scan_data = json.load(f)

    return render_template(
        "report.html",
        domain=scan_data["domain"],
        subdomains=scan_data.get("subdomains", []),
        open_ports=scan_data.get("open_ports", []),
        ai_summary=scan_data.get("ai_summary", ""),
        date=scan_data.get("date", ""),
        scan_data=scan_data,
    )


@app.route("/ask", methods=["POST"])
def ask():
    """AI assistant endpoint for the chat UI."""
    body = request.json
    question = body.get("question", "")
    context  = body.get("context", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    answer = ask_ai(question, context)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    print("[*] Starting Recon Framework server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
