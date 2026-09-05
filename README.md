# IPAudit API

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE)
[![Live API](https://img.shields.io/website?url=https%3A%2F%2Fipaudit.dev%2Fapi)](https://ipaudit.dev/api)
[![OpenAPI validated](https://img.shields.io/badge/OpenAPI-3.1-6ba539.svg)](openapi.yaml)

**Free, keyless IP trust-score API.** Send an IP address, get back a multi-source trust score, risk signals (VPN / proxy / Tor / hosting / bot), data confidence, and a per-source breakdown — the same intelligence that powers [ipaudit.dev](https://ipaudit.dev).

[中文文档](README.zh-CN.md)

## Quickstart

```bash
curl "https://ipaudit.dev/api/analyze?ip=8.8.8.8"
```

```json
{
  "ip": "8.8.8.8",
  "score": { "score": 90, "grade": "high", "signals": [ ... ] },
  "confidence": { "score": 88, "grade": "high", "healthySources": 7, "totalSources": 8 },
  "perSource": [ ... ]
}
```

A full annotated response lives in [docs/response-schema.md](docs/response-schema.md).

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/analyze?ip=<ip>&mode=remote\|self` | Full audit: trust score, risk signals, confidence, per-source detail |
| `GET /api/ip` | The caller's own IP address (`{ "ip": "...", "mode": "self", "cf": true }`) |
| `GET /api/badge/<ip>.svg?theme=light\|dark` | Embeddable SVG badge (`image/svg+xml`) |
| `GET /api/share/<ip>` | Shareable SVG result card |
| `GET /og/ip/<ip>` | Social preview card (PNG) |

Interactive playground: <https://ipaudit.dev/api>

## Authentication

None. The API is free and keyless — requests are rate-limited per client IP instead of being authenticated with tokens.

## Rate limits & caching

- **1,000 audits per client IP per day**, shared across the web tool, the API and the badge endpoints.
- Repeated audits of the same IP are served from a **one-hour cache**: polling an unchanged IP costs almost nothing and does not count against fresh upstream lookups.
- Exceeding the quota returns **`429`** with `{ "error": "rate limit exceeded", "limit": 1000 }`.
- Responses may include a per-source error row (e.g. an upstream rate-limiting us); treat each `perSource` row's `contributed` flag as the signal of whether that source answered.

See [docs/rate-limits.md](docs/rate-limits.md) for client best practices (backoff, caching, `Retry-After`).

## Errors

| Status | Meaning | Body |
|---|---|---|
| `400` | Missing or invalid `ip` parameter | `{ "error": "missing or invalid ip" }` |
| `429` | Daily quota exhausted | `{ "error": "rate limit exceeded", "limit": 1000 }` |
| `502` | Upstream data sources unavailable (image endpoints) | text |

## Example: embed a trust badge

```markdown
[![IP trust score](https://ipaudit.dev/api/badge/8.8.8.8.svg)](https://ipaudit.dev/ip/8.8.8.8)
```

[![IP trust score](https://ipaudit.dev/api/badge/8.8.8.8.svg)](https://ipaudit.dev/ip/8.8.8.8)

More snippets in [examples/github-badge.md](examples/github-badge.md).

## Data sources & attribution

Results aggregate (and cross-check) public data from ipwho.is, IPinfo, DB-IP, IP2Location, ip-api.com, MaxMind GeoLite2, Google DNS (DoH reverse DNS) and AbuseIPDB. Source terms and attribution requirements: [docs/data-sources.md](docs/data-sources.md).

## Spec & SDKs

- [`openapi.yaml`](openapi.yaml) — OpenAPI 3.1 spec, the single source of truth for these endpoints. Import it into Postman, Insomnia or Apifox, or generate a client SDK with OpenAPI Generator.
- The spec is linted in CI (Spectral) on every push.

## Feedback & data corrections

- API bugs / feature requests → [open an issue](../../issues) with the `api-bug` / `feature` template.
- "This IP's data looks wrong" → open an issue with the `data-correction` template and include the queried IP.

## Links

- Website & playground: <https://ipaudit.dev>
- API playground: <https://ipaudit.dev/api>
- Terms: <https://ipaudit.dev/terms> · Privacy: <https://ipaudit.dev/privacy>

## License

Documentation and spec are licensed under [CC BY 4.0](LICENSE). Using the API does not grant ownership of the returned data — see [docs/data-sources.md](docs/data-sources.md) for upstream attribution.
