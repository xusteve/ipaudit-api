# Embedding IPAudit trust badges in GitHub READMEs

The badge endpoint serves plain SVG, so it works anywhere Markdown or HTML renders images.

## Basic badge

```markdown
[![IP trust score](https://ipaudit.dev/api/badge/8.8.8.8.svg)](https://ipaudit.dev/ip/8.8.8.8)
```

[![IP trust score](https://ipaudit.dev/api/badge/8.8.8.8.svg)](https://ipaudit.dev/ip/8.8.8.8)

## Dark theme

```markdown
[![IP trust score](https://ipaudit.dev/api/badge/8.8.8.8.svg?theme=dark)](https://ipaudit.dev/ip/8.8.8.8)
```

## Your own IP

Badges render whatever IP is in the URL — point one at your server's address so visitors can check its reputation:

```markdown
[![My server's IP trust score](https://ipaudit.dev/api/badge/203.0.113.7.svg)](https://ipaudit.dev/ip/203.0.113.7)
```

## Notes

- Hot-linked badges served from cache are free and don't consume your daily quota.
- GitHub proxies external images through `camo.githubusercontent.com`; the badge still renders normally.
- Replace `8.8.8.8` with any IPv4/IPv6 address (URL-encode the colons in IPv6, e.g. `2606%3A4700%3A4700%3A%3A1111`).
