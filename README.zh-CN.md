# IPAudit API

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE)
[![Live API](https://img.shields.io/website?url=https%3A%2F%2Fipaudit.dev%2Fapi)](https://ipaudit.dev/api)
[![OpenAPI validated](https://img.shields.io/badge/OpenAPI-3.1-6ba539.svg)](openapi.yaml)

**免费、无需密钥的 IP 信任评分 API。** 传入一个 IP,返回多源信任评分、风险信号(VPN / 代理 / Tor / 托管 / 机器人)、数据置信度与逐源明细——与 [ipaudit.dev](https://ipaudit.dev) 网站使用同一套情报。

[English](README.md)

## 快速开始

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

带注释的完整响应见 [docs/response-schema.md](docs/response-schema.md)。

## 端点

| 端点 | 说明 |
|---|---|
| `GET /api/analyze?ip=<ip>&mode=remote\|self` | 完整审计:信任评分、风险信号、置信度、逐源明细 |
| `GET /api/ip` | 调用方自身 IP(`{ "ip": "...", "mode": "self", "cf": true }`) |
| `GET /api/badge/<ip>.svg?theme=light\|dark` | 可嵌入的 SVG 徽章(`image/svg+xml`) |
| `GET /api/share/<ip>` | 可分享的 SVG 结果卡片 |
| `GET /og/ip/<ip>` | 社交预览卡片(PNG) |

在线调试(playground):<https://ipaudit.dev/api>

## 认证

无。API 免费且无需密钥——按客户端 IP 限流,而非 token 鉴权。

## 限额与缓存

- **每个客户端 IP 每天 1,000 次审计**,与网页工具、徽章端点共享同一配额池。
- 对同一 IP 的重复审计走 **1 小时缓存**:轮询一个不变的 IP 几乎零成本,不会触发新的上游查询。
- 超出配额返回 **`429`**,响应体为 `{ "error": "rate limit exceeded", "limit": 1000 }`。
- 响应中可能包含某个数据源的失败行(例如该上游正在限流);请以每行 `perSource.contributed` 是否为 `true` 判断该源是否提供了数据。

客户端最佳实践(退避、缓存、`Retry-After`)见 [docs/rate-limits.md](docs/rate-limits.md)。

## 错误码

| 状态码 | 含义 | 响应体 |
|---|---|---|
| `400` | `ip` 参数缺失或非法 | `{ "error": "missing or invalid ip" }` |
| `429` | 当日配额已用尽 | `{ "error": "rate limit exceeded", "limit": 1000 }` |
| `502` | 上游数据源不可用(图片端点) | 文本 |

## 示例:嵌入信任徽章

```markdown
[![IP trust score](https://ipaudit.dev/api/badge/8.8.8.8.svg)](https://ipaudit.dev/ip/8.8.8.8)
```

[![IP trust score](https://ipaudit.dev/api/badge/8.8.8.8.svg)](https://ipaudit.dev/ip/8.8.8.8)

更多片段见 [examples/github-badge.md](examples/github-badge.md)。

## 数据源与署名

结果聚合并交叉比对来自 ipwho.is、IPinfo、DB-IP、IP2Location、ip-api.com、MaxMind GeoLite2、Google DNS(DoH 反向 DNS)与 AbuseIPDB 的公开数据。各数据源条款与署名要求:[docs/data-sources.md](docs/data-sources.md)。

## 规范与 SDK

- [`openapi.yaml`](openapi.yaml) — OpenAPI 3.1 规范,是这些端点的唯一权威定义。可导入 Postman、Insomnia 或 Apifox,也可用 OpenAPI Generator 生成客户端 SDK。
- 每次 push 时 CI 会用 Spectral 校验该规范。

## 反馈与数据纠错

- API 缺陷 / 功能建议 → [提交 issue](../../issues),使用 `api-bug` / `feature` 模板。
- "这个 IP 的数据看起来不对" → 使用 `data-correction` 模板并附上查询的 IP。

## 链接

- 网站与调试入口:<https://ipaudit.dev>
- API playground:<https://ipaudit.dev/api>
- 服务条款:<https://ipaudit.dev/terms> · 隐私政策:<https://ipaudit.dev/privacy>

## 许可证

文档与规范采用 [CC BY 4.0](LICENSE) 许可。调用 API 不代表获得返回数据的所有权——上游数据署名见 [docs/data-sources.md](docs/data-sources.md)。
