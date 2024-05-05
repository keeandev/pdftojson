# PDF to JSON API

https://pdftojson.vercel.app

This is a simple utility API that converts PDFs to structured JSON objects powered by [pdfminer.six](https://github.com/pdfminer/pdfminer.six).

```json
{
  "hash": "070dc0de7abc2a06",
  "total": 2,
  "pages": [
    "Page one contents....\nSecond line contents...",
    "Page two contents....\nSecond line contents..."
  ]
}
```

## Extra Goodies

<div>📄 Gets a total page count</div>
<div>#️⃣ Gives you a unique file hash (for your product)</div>
<div>📦 Requests are cached with <a href="https://upstash.com">Upstash</a> (10k commands/day)</div>
<div>🔒 Ratelimited (10s window, 2 max requests per window)</div>
