# Data sources & attribution

IPAudit aggregates and cross-checks public data from independent upstreams. Every audit fans out to these sources, then reconciles their answers (see [response-schema.md](response-schema.md) for the per-source detail).

| Source | Used for | Notes |
|---|---|---|
| IPinfo | Geolocation, ASN | Free tier |
| DB-IP | Geolocation, proxy/hosting flags | Free tier |
| IP2Location | Geolocation, proxy/hosting flags | Free tier (Lite) |
| ip-api.com | Geolocation, ASN, flags | Free for non-commercial use |
| MaxMind GeoLite2 | Geolocation | Requires attribution — [license](https://www.maxmind.com/en/geolite2/eula) |
| Google DNS (DoH) | Reverse DNS (PTR), IP→ASN mapping (Team Cymru origin data) | |
| FireHOL level-1 | Second threat vote (hijacked nets, botnet C2, DShield, Spamhaus DROP, bogons) | Community blocklist, GPLv2 — [repo](https://github.com/firehol/blocklist-ipsets), refreshed daily |
| AbuseIPDB | Abuse confidence score, threat flags | |

## What this means for you

- **Returned data is not yours to redistribute as a dataset.** The API gives you *a result for an IP you queried*, not a license to the underlying databases. Building your own copy of GeoLite2 or IPinfo by querying us IP-by-IP violates their terms and will be rate-limited out of existence.
- **Attribution.** If you build a visible product on top of the API, include a credit line such as *“IP intelligence by [ipaudit.dev](https://ipaudit.dev)”* — this also satisfies MaxMind's attribution requirement for the data we relay.
- **Accuracy.** Geolocation is city-level at best and occasionally wrong; that's inherent to the data industry, which is exactly why IPAudit cross-checks sources and reports contradictions instead of hiding them. Use `confidence` to decide how much to trust any single audit.
- Each upstream keeps its own terms. Links: [FireHOL blocklist-ipsets](https://github.com/firehol/blocklist-ipsets) · [IPinfo](https://ipinfo.io/terms) · [DB-IP](https://db-ip.com/db/terms) · [IP2Location](https://www.ip2location.com/terms-and-conditions) · [ip-api](https://ip-api.com) · [MaxMind GeoLite2 EULA](https://www.maxmind.com/en/geolite2/eula) · [AbuseIPDB](https://www.abuseipdb.com/terms).

## Reporting bad data

If a specific IP's result is clearly wrong (wrong country, wrong ASN), [open an issue](../../issues/new?template=data-correction.yml) with the IP and what you expected. Contradiction rows in `perSource` are expected sometimes; a *unanimously wrong* result is a bug worth reporting.
