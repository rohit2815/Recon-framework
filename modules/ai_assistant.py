import os
import sys
from anthropic import Anthropic

try:
    import readline  # enables arrow keys, backspace, and proper input buffering on Linux/macOS
except ImportError:
    pass  # Windows doesn't have readline; input still works

client = Anthropic()

SYSTEM_PROMPT = """You are an expert cybersecurity analyst and ethical hacking assistant 
embedded inside an automated reconnaissance framework. Your role is to:

1. Analyze scan results (subdomains, open ports, banners, CVEs) and explain findings clearly
2. Prioritize vulnerabilities by real-world exploitability and risk level
3. Suggest next steps for ethical penetration testing based on what was discovered
4. Explain CVEs and technical terms in plain English
5. Give actionable, specific recommendations

Always remind users to only test on systems they have explicit written authorization to test.
Format your responses with clear headings and bullet points for readability.
Be concise but thorough."""


def ask_ai(question, scan_context=None):
    """Ask the AI assistant a question, optionally with scan context."""
    messages = []

    if scan_context:
        content = f"Scan Context:\n{scan_context}\n\nQuestion: {question}"
    else:
        content = question

    messages.append({"role": "user", "content": content})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        return f"[!] AI assistant error: {e}"


def analyze_findings(scan_results_json):
    """Auto-analyze full scan results and return a structured risk summary."""
    prompt = """Analyze these reconnaissance findings and provide a structured report with:

## Risk Summary
- Overall risk score (1-10) with justification

## Top 3 Critical Findings
- List the most dangerous discoveries

## Attack Surface
- Key entry points an attacker would target first

## Recommended Next Steps
- Specific pentest actions to take (e.g., run Metasploit module X, check for default creds on port Y)

## Quick Wins
- Low-effort, high-impact things to check immediately

Keep it concise and actionable."""

    return ask_ai(prompt, scan_results_json)


def interactive_chat(scan_context):
    """Start an interactive CLI chat session with the AI assistant."""
    # Flush all previous output so the prompt never gets swallowed
    sys.stdout.flush()
    sys.stderr.flush()

    print("\n" + "="*60)
    print("  🤖 AI ASSISTANT — Ask anything about your scan results")
    print("  Type 'exit' or 'quit' to end the session")
    print("="*60 + "\n")
    sys.stdout.flush()

    while True:
        try:
            # Write prompt manually + flush BEFORE reading — prevents the
            # first character from being eaten when stdout isn't fully drained
            sys.stdout.write("You: ")
            sys.stdout.flush()
            question = sys.stdin.readline().strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[*] Exiting AI chat.")
            break

        if not question:
            continue
        if question.lower() in ["exit", "quit", "q"]:
            print("[*] Ending AI session.")
            break

        sys.stdout.write("\n🤖 AI: ")
        sys.stdout.flush()
        answer = ask_ai(question, scan_context)
        print(answer)
        print()
        sys.stdout.flush()
