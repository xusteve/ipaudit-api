# Response schema — `GET /api/analyze`

Field-by-field reference. The example below is a real, current response for `8.8.8.8` (abridged): Google's resolver scores 95 because exactly one upstream classifies its ASN as hosting — a textbook `disputed` signal.

## Top-level fields

| Field | Type | Description |
|---|---|---|
| `ip` | string | The audited address (normalized: IPv6 lowercased). |
| `mode` | `remote` \| `self` | Whether the query audited a given address or the caller's own. |
| `queryType` | `ipv4` \| `ipv6` | Address family of `ip`. |
| `country` | string | Consensus country name (majority view across sources). |
| `countryCode` | string | ISO 3166-1 alpha-2, e.g. `US`. |
| `region` | string | State / province, when known. |
| `city` | string | City, when known. |
| `asn` | string | Autonomous System Number announcing the address, e.g. `"15169"`. |
| `asnOrg` | string | Organization operating that AS, e.g. `"Google LLC"`. |
| `latitude` / `longitude` | number | Approximate location — city-level at best, **never** a street address. |
| `sources` | string[] | IDs of the sources consulted: `ipinfo`, `db-ip`, `ip2location`, `ip-api`, `maxmind`, `doh` (reverse DNS), `abuseipdb` — seven in total. |
| `reverseDns` | string \| null | PTR hostname, e.g. `dns.google`. |
| `threatInfo` | object | `{ "score": 0..100 }` — AbuseIPDB abuse-confidence score (higher = more abuse reports). |

## `raw` — detected risk indicators

```json
{ "proxy": false, "hosting": true, "bot": false, "geoAnomaly": false, "contradictions": 0 }
```

Boolean flags: `vpn`, `proxy`, `tor`, `hosting`, `bot`, `threat`, `geoAnomaly`. **A flag that is false may be omitted from the JSON — always read missing flags as `false`.**

This layer means "detected by at least one piece of evidence" (an upstream, or a derived hint such as the ASN owner / PTR hostname pattern). It does NOT mean the score deducted for it — deduction is decided by consensus, see [scoring.md](scoring.md). `contradictions` counts how many sources reported a country or ASN that disagrees with the majority view.

## `score` — the trust score

```json
{
  "score": 95, "grade": "high",
  "signals": [
    { "key": "vpn", "verdict": "consistent" },
    { "key": "hosting", "verdict": "disputed", "hits": 1, "healthy": 7, "deduct": 5 }
  ]
}
```

| Field | Description |
|---|---|
| `score` | 0–100. Higher = more trusted. Deductions are consensus-weighted: unanimous signals deduct in full, disputed signals deduct half (capped at 20). Full table: [scoring.md](scoring.md). |
| `grade` | `high` ≥ 70, `medium` ≥ 40, `low` ≥ 20, `suspicious` below. |
| `signals[].verdict` | `consistent` — unanimous (no source claims it, or every source does); `disputed` — minority claim, half deduction. |
| `signals[].hits` / `healthy` | Sources claiming the signal / sources that contributed. Present when detected. |
| `signals[].deduct` | Points actually deducted. Present when detected. |

A score of 0 means every contributing source agrees the address is hostile — a single noisy feed can never get an IP there.

## `confidence` — how much to trust this audit itself

```json
{ "score": 100, "grade": "high", "healthySources": 7, "totalSources": 7, "contradictions": 0 }
```

A score can be low either because the IP is risky *or* because few sources answered — `confidence` separates those two cases. Surface `score.grade` together with `confidence.grade`.

## `perSource` — one row per upstream

```json
{
  "id": "ipinfo", "name": "IPinfo",
  "contributed": true, "status": "ok",
  "country": "United States", "asn": "15169",
  "signals": {}, "conflict": { "country": false, "asn": false }
}
```

| Field | Description |
|---|---|
| `id` / `name` | Source identifier / display name: `ipinfo`, `db-ip`, `ip2location`, `ip-api`, `maxmind`, `doh` (reverse DNS), `abuseipdb`. |
| `contributed` | `true` when this source answered and fed the aggregate. **This is the field to branch on.** |
| `status` | `ok` or `error`. |
| `errorDetail` | Machine-readable reason when `status` is `error` (e.g. `HTTP 429`). |
| `rateLimited` | `true` when the upstream rate-limited us — transient by definition, so a retry later may succeed. |
| `country`, `countryCode`, `region`, `city`, `asn`, `asnOrg` | This source's own view of the address (present when it returned them). |
| `signals` | Boolean flags this source reported (`vpn`, `proxy`, `tor`, `hosting`, `bot`, `threat`). |
| `conflict` | `{ "country": bool, "asn": bool }` — whether this source's view disagrees with the consensus. |

Sources that fail still get a row (`contributed: false`, `status: "error"`); a persistent offender is skipped by a circuit breaker after repeated rate-limits.

## Caching semantics

A fresh audit is cached for **1 hour**. If fewer sources than needed were healthy when the audit ran, the result is cached for only **60 seconds** so it can self-heal. There is no `cached` flag in the response — assume any response may be up to an hour old and don't re-poll faster than that.
