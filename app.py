from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write("<h1>Hello World from Docker & Jenkins! </h1>".encode('utf-8'))

if __name__ == '__main__':
    print("Server starting on port 8000...")
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    server.serve_forever()