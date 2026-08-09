---
type: study
topic: "Web 与信息检索"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-检索建模与Web信息]]"
flow: knowledge
kind: concept
upstream: ["[[数据挖掘概述]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 直觉与动机

Web 信息检索（Web IR）是信息检索在互联网规模下的工程实现。与传统文档检索相比，Web IR 面临三大独特挑战：

1. **规模**：数十亿网页，持续动态更新
2. **质量**：网页质量参差不齐，垃圾页面（Spam）泛滥
3. **用户意图多样**：导航型（找网站）、信息型（查知识）、事务型（购物/下载）

理解 Web 搜索引擎架构是学习现代信息检索的基础，也是实现自定义搜索系统的理论起点。

---

## 📐 正式定义与系统架构

### 搜索引擎三大核心组件

```
            ┌──────────────────────────────────────────────┐
            │              搜索引擎架构                      │
            │                                              │
  互联网 ──▶ │  [爬虫 Crawler] ──▶ [索引 Indexer] ──▶ [排序器 Ranker] │──▶ 用户
            └──────────────────────────────────────────────┘
```

**① 爬虫（Web Crawler）**：
- 从种子 URL 出发，广度优先遍历 Web 超链接图
- 维护 URL 前端队列（Frontier），去重已爬取 URL
- 遵守 `robots.txt`（Robots Exclusion Protocol），避免爬取不允许的路径
- 礼貌性爬取：限制访问频率（Crawl Delay），避免对目标服务器造成 DDoS

**② 索引器（Indexer）**：
- 网页去重：SimHash 检测近重复（Near-Duplicate）内容
- 文本解析：提取 HTML 正文、标题、锚文本（Anchor Text）
- 构建倒排索引：$\text{Term} \to [(doc_1, pos_{11}, pos_{12}, \ldots), (doc_2, pos_{21}, \ldots), \ldots]$

**③ 排序器（Ranker）**：
- 离线计算页面权威性（PageRank）
- 在线计算查询-文档相关性（BM25、神经检索）
- 融合多路信号（相关性 + 权威性 + 时效性）

### URL 规范化（URL Canonicalization）

同一页面可能有多个 URL 形式，必须统一：

$$\text{http://www.example.com/page} \equiv \text{https://example.com/page/} \equiv \text{https://EXAMPLE.COM/Page}$$

规范化步骤：小写化 → HTTPS 优先 → 去除末尾斜杠 → 参数排序 → 设置 canonical 标签

### 网页去重：SimHash

SimHash 将文档映射为固定长度的 bit 向量，**Hamming 距离 ≤ 3** 的两个网页视为近重复：

$$\text{SimHash}(d) \in \{0,1\}^{64}, \quad \text{near-dup if } \text{Hamming}(h_1, h_2) \leq 3$$

---

## 💻 最小 Python 实现 — 简单 URL 规范化

```python
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl

def canonicalize_url(url: str) -> str:
    """URL 规范化：小写 scheme/host，排序参数，去除末尾斜杠"""
    parsed = urlparse(url)
    scheme = parsed.scheme.lower() or 'https'
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip('/') or '/'
    # 参数按字典序排序
    params = urlencode(sorted(parse_qsl(parsed.query)))
    return urlunparse((scheme, netloc, path, '', params, ''))

def is_allowed_by_robots(url: str, disallowed_paths: list[str]) -> bool:
    """简化版 robots.txt 遵守检查"""
    parsed = urlparse(url)
    path = parsed.path
    return not any(path.startswith(p) for p in disallowed_paths)

# 示例
urls = [
    "HTTP://WWW.Example.COM/Page/?b=2&a=1",
    "https://example.com/page?a=1&b=2",
]
for u in urls:
    print(canonicalize_url(u))
# 均输出: https://www.example.com/Page?a=1&b=2

disallowed = ['/admin/', '/private/']
print(is_allowed_by_robots('https://example.com/public/doc', disallowed))  # True
print(is_allowed_by_robots('https://example.com/admin/users', disallowed)) # False
```

---

## ⚠️ 常见误区与避坑指南

1. **爬虫不处理动态 JavaScript**：普通 HTTP 爬虫只能获取静态 HTML，无法执行 JS 渲染的内容。需要 Selenium/Playwright 或 Headless Chrome 渲染后再爬取。

2. **忽略 robots.txt 的法律风险**：在许多国家/地区，违反 robots.txt 爬取可能违反《计算机欺诈和滥用法》（CFAA）或服务条款，引发法律纠纷。

3. **混淆锚文本（Anchor Text）的价值**：指向某页面的超链接锚文本（如 `<a href="...">苹果官方网站</a>` 中的"苹果官方网站"）比页面自身文本更能反映该页面的主题，是早期 Google 的重要信号。

4. **URL 去重不等于内容去重**：即使 URL 不同，页面内容可能完全相同（如 HTTP vs HTTPS，www vs 非 www），必须同时做内容级去重（SimHash）。

5. **忽略 `canonical` 标签**：权威版本 URL 应在 HTML `<head>` 中声明 `<link rel="canonical" href="..."/>`，帮助搜索引擎合并重复页面的权重。

---

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```