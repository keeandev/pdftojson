from http.server import BaseHTTPRequestHandler

import json
import cgi
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams


class handler(BaseHTTPRequestHandler):

    def extract_pdf_content(pdf_file):
        # Extract text from PDF
        total_pages = 0
        page_contents = []

        with open(pdf_file, 'rb') as f:
            for page_num, page in enumerate(extract_text(f, laparams=LAParams(), output_type='dict')):
                total_pages += 1
                page_content = page['text']
                page_contents.append(
                    {'page': page_num + 1, 'content': page_content})

        return {'total_pages': total_pages, 'page_contents': page_contents}

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('Welcome to the PDFMiner API!\n'.encode('utf-8'))
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        pdf_content = self.extract_pdf_content(form["file"].file)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(pdf_content).encode())
