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

from viewer import HTMLViewer
from server import RequestServer


class MainWindow(QtGui.QMainWindow):
    def __init__(self, title, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(title)

        self.viewer = HTMLViewer(self)
        self.setCentralWidget(self.viewer)

        status = self.statusBar()
        status.setSizeGripEnabled(True)


def start_with(cui_server, title='Shareboard'):
    try:
        import sys
        app = QtGui.QApplication(sys.argv)

        server = RequestServer(cui_server)
        viewer = MainWindow(title)

        # server -> viewer
        server.request_recieved.connect(viewer.viewer.update)

        server.start()
        viewer.show()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MainWindow('Shareboard [DEBUG]')
    window.show()
    sys.exit(app.exec_())
