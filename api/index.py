from http.server import BaseHTTPRequestHandler

import json
import cgi
from io import BytesIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextContainer


class handler(BaseHTTPRequestHandler):

    def extract_pdf_content(self, pdf_content):
        total_pages = 0
        page_contents = []

        with BytesIO(pdf_content) as f:
            for page_num, page_layout in enumerate(extract_pages(f, laparams=LAParams(), caching=False)):
                total_pages += 1
                page_content = ''
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        page_content += element.get_text()
                page_contents.append(
                    {'page': page_num + 1, 'content': page_content.strip()})

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
