from http.server import BaseHTTPRequestHandler

import json
import os
from io import BytesIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextContainer
from upstash_redis import Redis
import xxhash

redis = Redis.from_env()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.send_header('Cache-Control', 'max-age=31536000, immutable')
        self.send_header('CDN-Cache-Control', 'max-age=31536000, immutable')
        self.end_headers()
        self.wfile.write('Welcome to the PDFMiner API!\n'.encode('utf-8'))
        self.wfile.write(
            f'Send a POST request to \'https://{os.environ["API_URL"]}\' with a binary file to extract its pages & contents!'.encode('utf-8'))
        return

    def do_POST(self):
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
                    result = {'total': total_pages, 'pages': page_contents}
                    redis.set(xxh.digest(), result)

            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        except Exception as e:
            self.send_error(500, 'Error extracting PDF content: {}'.format(e))
