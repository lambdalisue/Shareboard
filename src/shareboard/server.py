# vim: set fileencoding=utf-8 :
import urlparse
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler


class RequestServer(object):
    class HTTPPreviewRequestHandler(BaseHTTPRequestHandler):
        @property
        def request_server(self):
            return self.server.request_server

        def do_GET(self):
            try:
                if self.path == '/favicon.ico':
                    return
                queryset = urlparse.urlparse(self.path).query
                data = self.request_server.get_data_from_queryset(queryset)
                # emit request recieved
                if hasattr(self.request_server, 'thread'):
                    self.request_server.thread.emit_request_recieved(data)
                # respond data
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data)
            except Exception, e:
                print "Error:", e
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Unexpected error: %s" % e)

        def do_POST(self):
            try:
                # get pandoc filename from query string
                queryset = self.rfile.read(int(self.headers.getheader('Content-Length')))
                data = self.request_server.get_data_from_queryset(queryset)
                # emit request recieved
                if hasattr(self.request_server, 'thread'):
                    self.request_server.thread.emit_request_recieved(data)
                # respond OK
                self.send_response(200)
                self.end_headers()
                self.wfile.write('OK')
            except Exception, e:
                print "Error:", e
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Unexpected error: %s" % e)

        def log_message(self, format, *args):
            if not self.request_server.silent:
                # `super(cls, self).log_message(format, *args)` did not work
                BaseHTTPRequestHandler.log_message(self, format, *args)
            return None

    def __init__(self, host, port, callback=None, silent=False):
        super(RequestServer, self).__init__()
        self.host = host
        self.port = port
        self.callback = callback
        self.silent = silent
        self.httpd = HTTPServer((host, port), self.HTTPPreviewRequestHandler)
        self.httpd.request_server = self
        self.previous_data = ''

    def start(self):
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            if hasattr(self, 'qApp'):
                exit(0)
                self.qApp.quit()
            else:
                exit(0)

    def get_data_from_queryset(self, queryset):
        queryset = urlparse.parse_qs(queryset, 1)
        data = queryset.get('data', [self.previous_data])[0]
        # data is passed as utf-8
        data = unicode(data, 'utf-8')
        # callback
        if self.callback and callable(self.callback):
            data = self.callback(data)
        # store this data as previous_data
        self.previous_data = data
        return data


def create_server_thread(server):
    from PySide.QtGui import qApp
    from PySide.QtCore import Signal
    from PySide.QtCore import QThread

    class RequestServerThread(QThread):
        request_recieved = Signal(unicode)

        def __init__(self, server):
            super(RequestServerThread, self).__init__()
            self.server = server
            self.server.thread = self

        def run(self):
            self.server.start()

        def emit_request_recieved(self, data):
            # emit
            self.request_recieved.emit(data)
    server.qApp = qApp
    return RequestServerThread(server)
