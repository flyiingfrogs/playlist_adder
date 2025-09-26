import http.server
import socketserver
import urllib.parse


class AuthCodeCatcher:
    def __init__(self):
        self.auth_code = None

    def make_handler(self):
        catcher = self

        class SpotifyAuthHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parsed_path = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(parsed_path.query)

                if "code" in query:
                    catcher.auth_code = query["code"][0]
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<h1>Authorization successful!</h1>You can close this window.")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"<h1>Error: Authorization code not found.</h1>")

            def log_message(self, format, *args):
                return  # Disable logging to console

        return SpotifyAuthHandler

    def run_once(self, host="127.0.0.1", port=8888):
        with socketserver.TCPServer((host, port), self.make_handler()) as httpd:
            httpd.handle_request()
        return self.auth_code