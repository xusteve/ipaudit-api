/**
 * IPAudit API — Node 18+ (built-in fetch), no dependencies.
 *
 * Run: node analyze.js 8.8.8.8
 */
const BASE = 'https://ipaudit.dev';

async function analyze(ip) {
  const res = await fetch(`${BASE}/api/analyze?ip=${encodeURIComponent(ip)}`);

  if (res.status === 429) {
    // Daily quota exhausted. Honor Retry-After (we get seconds until the next
    // UTC day) or back off until tomorrow — do not hot-loop.
    const retryAfter = Number(res.headers.get('retry-after') || 60);
    throw new Error(`Rate limited; retry after ~${retryAfter}s`);
  }
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

const ip = process.argv[2] || '8.8.8.8';
const audit = await analyze(ip);

console.log(`IP          ${audit.ip} (${audit.queryType})`);
console.log(`Location    ${audit.city || '?'}, ${audit.countryCode || '?'}`);
console.log(`Network     AS${audit.asn} ${audit.asnOrg || ''}`);
console.log(`Reverse DNS ${audit.reverseDns ?? '—'}`);
console.log(`Trust score ${audit.score.score}/100 (${audit.score.grade})`);
console.log(`Confidence  ${audit.confidence.score}/100 ` +
  `(${audit.confidence.healthySources}/${audit.confidence.totalSources} sources healthy)`);
console.log(`Flags       ` +
  JSON.stringify(Object.fromEntries(Object.entries(audit.raw).filter(([, v]) => v === true))));
console.log('Per source:');
for (const s of audit.perSource) {
  console.log(`  ${s.contributed ? '✓' : '✗'} ${s.name}${s.errorDetail ? ` — ${s.errorDetail}` : ''}`);
}
