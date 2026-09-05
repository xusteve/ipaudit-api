name: API bug report
about: Something about an endpoint isn't working the way the docs say.
title: "[api] "
labels: ["api-bug"]
---

**Endpoint**
- [ ] `/api/analyze`
- [ ] `/api/ip`
- [ ] `/api/badge/<ip>.svg`
- [ ] `/api/share/<ip>`
- [ ] `/og/ip/<ip>`

**What I expected**
<!-- What the docs / past behavior said should happen. -->

**What happened**
<!-- What you actually saw, including the exact response body and status code if possible. -->

**Reproduction**
```bash
curl -i 'https://ipaudit.dev/api/...'
```

**Other**
<!-- Browser, language, IP you queried (so we can reproduce), anything else relevant. -->