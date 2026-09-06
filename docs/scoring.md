# Scoring rules (full transparency)

The trust score starts at **100** and deducts for detected risk signals. Two ideas define the model:

1. **Consensus-weighted deductions.** What matters is not *whether* a signal was claimed, but *how many of the contributing upstreams claim it*.
2. **Score and confidence are separate.** Thin data lowers `confidence`, never the score itself.

## Deduction table (full weight — unanimous)

| Signal | Deduction |
|---|---|
| `threat` | −35 (reported by AbuseIPDB **and** the FireHOL level-1 blocklist — two independent threat sources; both claiming = unanimous full weight, either alone = disputed) |
| `bot` | −30 |
| `tor` | −25 |
| `vpn` | −20 |
| `proxy` | −15 |
| `geo` (3+ sources disagree on the country) | −15 |
| `hosting` / datacenter | −10 |

## Verdicts

| `verdict` | Meaning | Deduction |
|---|---|---|
| `consistent` | Unanimous: no contributing source claims the signal (no deduction), or **every** contributing source claims it (full deduction). | 0 or full |
| `disputed` | Only a minority of sources claim the signal (or it comes from a single derived hint such as the ASN owner name / PTR hostname pattern). | **half, capped at 20** |

The response reports `hits` (sources claiming) and `healthy` (sources contributing) alongside every detected signal, so you can reproduce the verdict yourself.

## Grade bands

| Score | Grade |
|---|---|
| ≥ 70 | `high` |
| ≥ 40 | `medium` |
| ≥ 20 | `low` |
| < 20 | `suspicious` |

## Worked examples

**8.8.8.8 (Google Public DNS) → 95 `high`.** MaxMind-classified hosting on Google's ASN is the only whisper of "hosting", plus the datacenter ASN hint — 1 of 7 sources → `disputed` → −5. Everything else unanimous clean.

**A Tor exit node whose abuse flags come from a single intel feed → ~49 `medium`.** tor −13, threat −18, hosting −5 (each 1-of-7 disputed). Under the old single-source model this address scored 0; now the score reads as "contested evidence", and the per-source table shows exactly who said what. If more upstreams confirm the signals, the deductions grow to full weight on the next audit.

## What does NOT affect the score

- Missing sources / upstream errors → `confidence` only.
- Cross-source country/ASN contradictions → `confidence` + the `contradictions` field (and the public disputes table on the leaderboard), not the score.
- The caller's identity, geography, or query volume.
