import http.server
import socketserver
import threading
import http.client
import json

messages = []

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Disable logging of requests
        pass

    def do_POST(self):
        if self.path == '/Terminal':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            message = data['message']
            messages.append(message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/fetch_messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_body = json.dumps({'messages': messages})
            self.wfile.write(response_body.encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('c:/Users/HP/OneDrive/Documents/SwarmDrones/Server_Test/index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

def start_server(port=8888):
    print("Starting server...")
    handler = MyRequestHandler
    with socketserver.TCPServer(('0.0.0.0', port), handler) as httpd:
        httpd.serve_forever()

def send(data, ip='192.168.190.101', port=8888):
    conn = http.client.HTTPConnection(ip, port)
    headers = {'Content-type': 'application/json'}
    body = json.dumps({'message': data})
    conn.request('POST', '/Terminal', body, headers)
    response = conn.getresponse()
    print("Response from server:", response.read().decode())
