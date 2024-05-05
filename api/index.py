from upstash_ratelimit import Ratelimit, FixedWindow
from http.server import BaseHTTPRequestHandler
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from pdfminer.layout import LAParams
from upstash_redis import Redis
from io import BytesIO
import xxhash
import json
import os

redis = Redis.from_env()

ratelimit = Ratelimit(
    redis=Redis.from_env(),
    limiter=FixedWindow(max_requests=2, window=10),
    prefix="upstash-ratelimit",
)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.send_header('Cache-Control', 'max-age=31536000, immutable')
        self.send_header('CDN-Cache-Control', 'max-age=31536000, immutable')
        self.end_headers()
        self.wfile.write('Welcome to the PDF to JSON API (pdfminer.six API)!\n'.encode('utf-8'))
        self.wfile.write(
            f'Send a POST request to \'https://{os.environ["API_URL"]}\' with a binary file to extract its pages & contents!'.encode('utf-8'))
        return

    def do_POST(self):
        response = ratelimit.limit("api")

        if not response.allowed:
            self.send_response(429)
            self.wfile.write("Too Many Requests".encode("utf-8"))

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try:
            xxh = xxhash.xxh3_64()
            total_pages = 0
            page_contents = []

            with BytesIO(body) as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    xxh.update(chunk)

                result = redis.get(xxh.hexdigest())

                if not result:
                    for _, page_layout in enumerate(extract_pages(f, laparams=LAParams())):
                        total_pages += 1
                        page_content = ''
                        for element in page_layout:
                            if isinstance(element, LTTextContainer):
                                page_content += element.get_text()
                        page_contents.append(page_content.strip())
                    result = json.dumps({'total': total_pages, 'pages': page_contents})
                    redis.set(xxh.hexdigest(), result)

            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(result.encode("utf-8"))
        except Exception as e:
            self.send_error(500, 'Error extracting PDF content: {}'.format(e))
