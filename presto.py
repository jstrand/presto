from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import re
import os

class SaveRequest(BaseHTTPRequestHandler):

    valid_post_pattern = re.compile(r'^(\/[0-9a-z\-_]+)+$')
    valid_get_pattern = re.compile(r'^(\/[0-9a-z\-_]+)*\/?$')

    def valid_get(self):
        return self.valid_get_pattern.match(self.path)

    def valid_post(self):
        return self.valid_post_pattern.match(self.path)

    def do_GET(self): 
        if not self.valid_get():
            self.log_error(self.path + ' not allowed')
            self.send_response(400, 'Invalid path')
            self.end_headers()
            return
    
        file_path = 'data' + self.path

        if not os.path.exists(file_path):
            self.send_response(404, "Not found")
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

        with open(file_path, 'rb') as get_file:
            self.wfile.write(get_file.read())

    def do_POST(self):
       
        if not self.valid_post():
            self.log_error(self.path + ' not allowed')
            self.send_response(400, 'Invalid path')
            self.end_headers()
            return

        file_path = 'data' + self.path
        file_location = os.path.dirname(file_path)
        if not os.path.exists(file_location):
            os.makedirs(os.path.dirname(file_path))

        content_length = int(self.headers.get('Content-Length'))
        content = self.rfile.read(content_length)

        with open(file_path, 'wb') as output_file:
            output_file.write(content)

        print(self.path)

        self.send_response(201)
        self.end_headers()

class PrestoServer:
    def __init__(self, host, port):
        server_address = (host, port)
        self.httpd = HTTPServer(server_address, SaveRequest)
        self.log = logging.getLogger('PrestoServer')

    def serve_forever(self):
        self.log.info('Serving Presto on ' + self.httpd.server_name + ':' + str(self.httpd.server_port))
        self.httpd.serve_forever()
