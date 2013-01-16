#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Author:   lambdalisue (lambdalisue@hashnote.net)
# URL:      http://hashnote.net/
# License:  MIT license
# Created:  2013-01-16
#
try:
    from PySide import QtCore
    from PySide import QtGui
except ImportError:
    from PyQt4 import QtCore
    from PyQt4 import QtGui


class RequestServer(QtCore.QThread):
    def __init__(self, cui_server):
        super(RequestServer, self).__init__()
        self.cui_server = cui_server
        self.cui_server.httpd.emitter = self

    def run(self):
        self.cui_server.start()

    def emit_request_recieved(self, value):
        self.request_recieved.emit(value)

    # --- signal
    request_recieved = QtCore.Signal(unicode)
