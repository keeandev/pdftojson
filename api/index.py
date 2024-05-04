from http.server import BaseHTTPRequestHandler

import json
import cgi
from io import BytesIO
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams


class handler(BaseHTTPRequestHandler):

    def extract_pdf_content(self, pdf_content):
        total_pages = 0
        page_contents = []

        with BytesIO(pdf_content) as f:
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
    content_type, params = cgi.parse_header(self.headers['content-type'])

    if content_type == 'multipart/form-data':
        boundary = params['boundary'].encode()

        try:
            form_data = cgi.parse_multipart(self.rfile, {'boundary': boundary})
            if b'file' in form_data:
                pdf_content = form_data[b'file'][0]
                result = self.extract_pdf_content(pdf_content)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_error(400, 'Missing \'file\' in FormData.')
        except Exception as e:
            self.send_error(500, 'Error extracting PDF content: {}'.format(e))
    else:
        self.send_error(400, 'Bad Request: Unsupported Content-Type')
