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
    from PySide.QtWebKit import QWebView
    from PySide.QtNetwork import QNetworkProxyFactory
except ImportError:
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from PyQt4.QtWebKit import QWebView
    from PyQt4.QtNetwork import QNetworkProxyFactory


# Use system proxy settings
QNetworkProxyFactory.setUseSystemConfiguration(True)


class HTMLViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(HTMLViewer, self).__init__(parent)

        self.view = QWebView(self)
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        # Create ContextMenu
        context_menu = QtGui.QMenu(self.view)
        def open_context_menu(point):
            context_menu.exec_(self.view.mapToGlobal(point))
        self.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(open_context_menu)

        action = QtGui.QAction('&Back', self,
                shortcut=QtGui.QKeySequence.Back,
                statusTip="Click to go back",
                triggered=self.view.back)
        action.setShortcut('Backspace')
        context_menu.addAction(action)

        action = QtGui.QAction('&Forward', self,
                shortcut=QtGui.QKeySequence.Forward,
                statusTip="Click to go forward",
                triggered=self.view.forward)
        action.setShortcut('Shift + Backspace')
        context_menu.addAction(action)

        action = QtGui.QAction('&Reload', self,
                shortcut=QtGui.QKeySequence.Refresh,
                statusTip="Click to refresh",
                triggered=self.view.reload)
        context_menu.addAction(action)
        context_menu.addSeparator()

        action = QtGui.QAction('&Print', self,
                shortcut=QtGui.QKeySequence.Print,
                statusTip="Click to print",
                triggered=self.print_)
        context_menu.addAction(action)
        
    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())

    def print_(self):
        printer = QtGui.QPrinter()
        printer_dialog = QtGui.QPrintDialog(printer, self.view)
        if printer_dialog.exec_() != QtGui.QDialog.Accepted:
            # do nothing
            return
        # printout the view with selected printer
        self.view.print_(printer)

    # --- slots
    @QtCore.Slot(unicode, unicode)
    def update(self, value, base_url='file:///'):
        # save vertical/horizontal scrollbar value
        m = self.view.page().mainFrame()
        v = m.scrollBarValue(QtCore.Qt.Vertical)
        h = m.scrollBarValue(QtCore.Qt.Horizontal)
        # set new HTML (value should be unicode)
        self.view.setHtml(value, QtCore.QUrl(base_url))
        # update vertical/horizontal scrollbar value
        m = self.view.page().mainFrame()
        m.setScrollBarValue(QtCore.Qt.Vertical, v)
        m.setScrollBarValue(QtCore.Qt.Horizontal, h)
