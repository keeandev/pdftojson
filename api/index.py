from http.server import BaseHTTPRequestHandler

import json
import cgi
from io import BytesIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams


class handler(BaseHTTPRequestHandler):

    def extract_pdf_content(self, pdf_content):
        total_pages = 0
        page_contents = []

        with BytesIO(pdf_content) as f:
            for page_num, page in enumerate(extract_text_to_fp(f, laparams=LAParams(), output_type='dict')):
                total_pages += 1
                page_content = page['text']
                page_contents.append(
                    {'page_number': page_num+1, 'content': page_content})

        return {'total_pages': total_pages, 'page_contents': page_contents}

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('Welcome to the PDFMiner API!\n'.encode('utf-8'))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try:
            result = self.extract_pdf_content(body)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_error(500, 'Error extracting PDF content: {}'.format(e))
