# vim: set fileencoding=utf-8 :
import cgi
import urlparse
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler


REQUEST_IGNORE_PATHS = (
        '/favicon.ico',
    )


class HTTPPreviewRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in REQUEST_IGNORE_PATHS:
            return
        # respond data
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.text)

    def do_POST(self):
        try:
            request = cgi.FieldStorage(
                    self.rfile, self.headers, environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                })
            if 'text' not in request:
                msg = 'The request should contain "text" field to set new text'
                self.send_response(400, msg)
                self.end_headers()
                self.wfile.write(msg)
                return
            # decode text to unicode
            text = unicode(request['text'].value, self.server.encoding)
            # modify the text with callback if it's specified
            if self.server.callback:
                text = self.callback(text)
            # store the value
            self.text = text
            # emit request recieved if it's required
            if hasattr(self.server, 'emitter'):
                self.server.emitter.emit_request_recieved(text)
            # respond OK
            self.send_response(200)
            self.end_headers()
            self.wfile.write('OK')
        except Exception, e:
            print "Error:", e
            self.send_response(500, e)
            self.end_headers()
            self.wfile.write("Unexpected error: %s" % e)

    def log_message(self, format, *args):
        if not self.server.silent:
            # `super(cls, self).log_message(format, *args)` did not work
            BaseHTTPRequestHandler.log_message(self, format, *args)
        return None


class RequestServer(object):
    def __init__(self, host, port, encoding='utf-8', callback=None, silent=False):
        super(RequestServer, self).__init__()
        self.httpd = HTTPServer((host, port), HTTPPreviewRequestHandler)
        self.httpd.encoding = encoding
        self.httpd.callback = callback
        self.httpd.silent = silent

    def start(self):
        self.httpd.serve_forever()
