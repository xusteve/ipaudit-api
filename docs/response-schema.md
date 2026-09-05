# Response schema — `GET /api/analyze`

Field-by-field reference. The example response is a real, complete response for `8.8.8.8` (kept verbatim, including one upstream error row — that's the normal way a healthy audit looks when one source is having a bad day).

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
| `sources` | string[] | IDs of all sources consulted for this audit. |
| `reverseDns` | string \| null | PTR hostname, e.g. `dns.google`. |
| `threatInfo` | object | `{ "score": 0..100 }` — AbuseIPDB abuse-confidence score (higher = more abuse reports). |

## `raw` — aggregated risk flags

```json
{ "proxy": false, "hosting": true, "bot": false, "geoAnomaly": false, "contradictions": 0 }
```

Boolean flags: `vpn`, `proxy`, `tor`, `hosting`, `bot`, `threat`, `geoAnomaly`. **A flag that is false may be omitted from the JSON — always read missing flags as `false`.**

`contradictions` counts how many sources reported a country or ASN that disagrees with the majority view. `geoAnomaly` flags "impossible travel"-style results (the same IP attributed to far-apart locations by different sources).

## `score` — the trust score

```json
{ "score": 90, "grade": "high", "signals": [ { "key": "hosting", "verdict": "conflict" } ] }
```

| Field | Description |
|---|---|
| `score` | 0–100. Higher = more trusted. Starts at 100; each confirmed risk signal deducts (hosting −10, geo anomaly −15, VPN −20, proxy −25, Tor −25, bot −30, threat −35). |
| `grade` | `high` ≥ 80, `medium` ≥ 60, `low` ≥ 40, `suspicious` below. |
| `signals[]` | One entry per signal key (`vpn`, `proxy`, `tor`, `hosting`, `bot`, `threat`, `geo`); `verdict` is `consistent` (sources agree), `conflict` (sources disagree — shown to the user, scored cautiously) or `unknown`. |

## `confidence` — how much to trust this audit itself

```json
{ "score": 88, "grade": "high", "healthySources": 7, "totalSources": 8, "contradictions": 0 }
```

A score can be low either because the IP is risky *or* because few sources answered — `confidence` separates those two cases. Prefer consumers to surface `score.grade` together with `confidence.grade`.

## `perSource` — one row per upstream

```json
{
  "id": "ipwho.is", "name": "ipwho.is",
  "contributed": false, "status": "error",
  "errorDetail": "HTTP 429", "rateLimited": true,
  "signals": {}, "conflict": { "country": false, "asn": false }
}
```

| Field | Description |
|---|---|
| `id` / `name` | Source identifier / display name: `ipwho.is`, `ipinfo`, `db-ip`, `ip2location`, `ip-api`, `maxmind`, `doh` (reverse DNS), `abuseipdb`. |
| `contributed` | `true` when this source answered and fed the aggregate. **This is the field to branch on.** |
| `status` | `ok` or `error`. |
| `errorDetail` | Machine-readable reason when `status` is `error` (e.g. `HTTP 429`). |
| `rateLimited` | `true` when the upstream rate-limited us — transient by definition, so a retry later in the day may succeed. |
| `country`, `countryCode`, `region`, `city`, `asn`, `asnOrg` | This source's own view of the address (present when it returned them). Comparing these across rows is how you reproduce the contradiction count. |
| `signals` | Boolean risk flags this specific source reported. |
| `conflict` | `{ "country": bool, "asn": bool }` — whether this source's view disagrees with the consensus. |

## Caching semantics

A fresh audit is cached for **1 hour**. If fewer sources than needed were healthy when the audit ran, the result is cached for only **60 seconds** so it can self-heal. There is no `cached` flag in the response — assume any response may be up to an hour old and don't re-poll faster than that.
