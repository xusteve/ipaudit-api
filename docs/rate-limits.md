# Rate limits & client best practices

## The numbers

- **1,000 audits per client IP per day** (UTC day). The counter resets at midnight UTC.
- The quota is shared across **all** audit paths: the web tool, `/api/analyze`, `/api/badge`, `/api/share` and `/og/ip`.
- Repeated audits of the same address are served from a **1-hour edge cache** and a cache hit costs you nothing.
- `GET /api/ip` (echoing your own address) is not an audit and is not counted.

## 429 responses

```json
{ "error": "rate limit exceeded", "limit": 1000 }
```

The `Retry-After` header is set to the number of seconds until the counter resets. Page responses (as opposed to the JSON API) return the same quota semantics with a plain-text body.

## Best practices

1. **Cache on your side.** If you audit the same IPs repeatedly, cache the response for an hour. Your cache and ours then compose: one real upstream audit per hour per IP, free everywhere else.
2. **Never hot-loop on 429.** Honor `Retry-After`; if it's large, schedule the work for after the UTC reset instead of busy-waiting.
3. **Batch-wise, not burst-wise.** The quota is daily, not per-second — you can't "use it up faster", but you also can't borrow from tomorrow. Spread bulk jobs across the day.
4. **Treat `502` on image endpoints as transient.** It means upstream sources were unreachable; retry with exponential backoff (1s → 5s → 30s).
5. **IPv6 addresses:** URL-encode the colons (`2606%3A4700%3A4700%3A%3A1111`) when putting an address in a path.
6. **Identify yourself.** Set a descriptive `User-Agent` (e.g. `myapp/1.2 (+https://example.com)`) so we can tell legitimate integrations from abuse when something goes wrong.

## Fair use

The free tier exists so developers can build things — scraping every IP you can think of is a different use case. If you need more than the shared daily quota, [open an issue](../../issues) describing your use case before building around the limits.
