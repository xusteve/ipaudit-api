name: Data correction
about: An IP's audit result looks unambiguously wrong and you want it investigated.
title: "[data] "
labels: ["data-correction"]
---

**IP queried**
<!-- e.g. 8.8.8.8 — only one IP per issue, please. -->

**What IPAudit returned**
```json
{ "country": "...", "countryCode": "...", "asn": "...", "asnOrg": "..." }
```

**What it should have been (and how you know)**
<!-- Cite a public source: the IP operator's ASN record, the operator's documented address range, a registration database. Avoid "I think" reports — focus on facts. -->

**Optional: per-source row**
<!-- If you can identify which `perSource` row is the outlier, paste it here. -->