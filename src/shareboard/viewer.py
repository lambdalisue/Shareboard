#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import QWebView


TITLE = 'Shareboard Viewer'


class Viewer(object):
    class ViewerWidget(QWidget):
        def __init__(self, parent=None):
            super(Viewer.ViewerWidget, self).__init__(parent)
            self.view = QWebView(self)
            self.view.setContextMenuPolicy(Qt.CustomContextMenu)
            self.view.customContextMenuRequested.connect(self.openContextMenu)

            layout = QVBoxLayout(self)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.view)

            self.view.show()

        @Slot(unicode)
        def update_preview(self, value):
            # save vertical/horizontal scrollbar value
            m = self.view.page().mainFrame()
            v = m.scrollBarValue(Qt.Vertical)
            h = m.scrollBarValue(Qt.Horizontal)
            # set new HTML
            self.view.setHtml(value)
            # update vertical/horizontal scrollbar value
            m = self.view.page().mainFrame()
            m.setScrollBarValue(Qt.Vertical, v)
            m.setScrollBarValue(Qt.Horizontal, h)

        def openContextMenu(self, position):
            menu = QMenu()
            printAction = menu.addAction('Print')
            quitAction = menu.addAction('Quit')
            action = menu.exec_(self.view.mapToGlobal(position))

            if action == quitAction:
                qApp.quit()
            elif action == printAction:
                printer = QPrinter()
                dialog = QPrintDialog(printer, self.view)
                if dialog.exec_() != QDialog.Accepted:
                    return
                self.view.print_(printer)

    class Window(QMainWindow):
        def __init__(self, parent=None):
            super(Viewer.Window, self).__init__(parent)
            self.viewer = Viewer.ViewerWidget(self)
            self.setCentralWidget(self.viewer)
            self.setWindowTitle(TITLE)

            status = self.statusBar()
            status.setSizeGripEnabled(True)

            self.statusLabel = QLabel("")
            status.addWidget(self.statusLabel, 1)

            exitAction = QAction('&Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.setStatusTip('Exit application')
            exitAction.triggered.connect(qApp.quit)

            menubar = self.menuBar()
            fileMenu = menubar.addMenu('&File')
            fileMenu.addAction(exitAction)

            self.viewer.view.loadFinished.connect(self.loadFinished)
            self.viewer.view.loadProgress.connect(self.loading)

        @Slot(bool)
        def loadFinished(self, flag):
            self.statusLabel.setText("Done")

        @Slot(int)
        def loading(self, percent):
            self.statusLabel.setText("Loading: %d%%" % percent)

    def __init__(self, request_server):
        self.request_server = request_server

    def start(self):
        app = QApplication(sys.argv)
        window = self.Window()
        # connect to request server
        viewer = window.viewer
        request_recieved = self.request_server.thread.request_recieved
        request_recieved.connect(viewer.update_preview)
        window.show()
        sys.exit(app.exec_())
