# PDF to JSON API

https://pdftojson.vercel.app

This is a simple utility API that converts PDFs to structured JSON objects, powered by [pdfminer.six](https://github.com/pdfminer/pdfminer.six).

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
<div>🔒 Ratelimited (1s window, max 2 requests/window)</div>

## What I Learned
- The value of caching & ratelimiting
- How to create an API in Python (I've always built them in TypeScript before this)
- Hashes don't have to be long? What?
