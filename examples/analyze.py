"""IPAudit API — Python 3.9+, stdlib only (requests works the same way).

Run: python3 analyze.py 8.8.8.8
"""
import json
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://ipaudit.dev"


def analyze(ip: str) -> dict:
    url = f"{BASE}/api/analyze?{urllib.parse.urlencode({'ip': ip})}"
    req = urllib.request.Request(url, headers={"User-Agent": "ipaudit-api-example/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # Daily quota exhausted — wait (Retry-After is seconds) or run tomorrow.
            retry_after = int(e.headers.get("Retry-After", "60"))
            print(f"Rate limited; retry after ~{retry_after}s", file=sys.stderr)
            time.sleep(retry_after)
            return analyze(ip)
        raise


if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
    audit = analyze(ip)

    print(f"IP          {audit['ip']} ({audit['queryType']})")
    print(f"Location    {audit.get('city', '?')}, {audit.get('countryCode', '?')}")
    print(f"Network     AS{audit.get('asn')} {audit.get('asnOrg', '')}")
    print(f"Reverse DNS {audit.get('reverseDns') or '—'}")
    print(f"Trust score {audit['score']['score']}/100 ({audit['score']['grade']})")
    conf = audit["confidence"]
    print(f"Confidence  {conf['score']}/100 ({conf['healthySources']}/{conf['totalSources']} sources healthy)")
    print("Per source:")
    for s in audit["perSource"]:
        mark = "✓" if s["contributed"] else "✗"
        extra = f" — {s['errorDetail']}" if s.get("errorDetail") else ""
        print(f"  {mark} {s['name']}{extra}")
