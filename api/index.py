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
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        if 'Content-Type' in self.headers:
            content_type = self.headers['Content-Type']
            if content_type.startswith('multipart/form-data'):
                form = {}
                for item in body.decode('utf-8').split('\r\n'):
                    if item.startswith('Content-Disposition'):
                        _, params = item.split('; ')
                        name = params.split('=')[1].strip('"')
                        form[name] = body.split(item.encode())[
                            1].strip().strip(b'--\r\n')

        if 'file' in form:
            pdf_content = form['file']
            try:
                result = self.extract_pdf_content(pdf_content)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_error(
                    500, 'Error extracting PDF content: {}'.format(e))
            return
        else:
            self.send_error(400, 'Missing \'file\' in FormData.')
