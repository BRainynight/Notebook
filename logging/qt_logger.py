import logging, sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont 
from PyQt5.QtWidgets import *
from logpkg import get_logger
Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot
logger = get_logger(rootName="__main__", timeFlag=False, log_dir=".")

# 把 logging 的內容放在 qt 的 textbrowser 之類的
class Signaller(QtCore.QObject):
    ''' 
    https://gist.github.com/vsajip/a87bd7f4234510b4fd6bdcd4ffea376d
    Signals need to be contained in a QObject or subclass in order to be correctly 
    initialized.
    '''
    signal = Signal(str, logging.LogRecord)

class QtHandler(logging.Handler):
    '''
    https://gist.github.com/vsajip/a87bd7f4234510b4fd6bdcd4ffea376d
    Output to a Qt GUI is only supposed to happen on the main thread. So, this
    handler is designed to take a slot function which is set up to run in the main
    thread. In this example, the function takes a string argument which is a
    formatted log message, and the log record which generated it. The formatted
    string is just a convenience - you could format a string for     output any way
    you like in the slot function itself.

    You specify the slot function to do whatever GUI updates you want. The handler
    doesn't know or care about specific UI elements.
    '''
    def __init__(self, slotfunc, *args, **kwargs):
        super(QtHandler, self).__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slotfunc)

    def emit(self, record):
        s = self.format(record)
        self.signaller.signal.emit(s, record)

class Layout(QWidget):
    html_format = {
        logging.DEBUG: ("black", "1"),
        logging.INFO: ("green", "1"),
        logging.WARNING: ("blue", "2"),
        logging.ERROR: ("red", "3"),
        logging.CRITICAL: ("purple", "3"),
    }
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        
        self.count = 0 

        grid = QGridLayout()


        h = QtHandler(self.update_browser)
        self.handler = h
        h.setFormatter(logging.Formatter('%(message)s'))
        h.setLevel(logging.DEBUG)
        logger.addHandler(h)

        self.browser = QTextBrowser(self)
        self.browser.setFont(QFont('Times', 12))
        self.browser.append("Open")

        self.btn_add = QPushButton("Click!", self)
        self.btn_add.clicked.connect(self.record)

        self.btn_reset = QPushButton("Reset", self)
        self.btn_reset.clicked.connect(self.reset)


        grid.addWidget(self.browser, 0, 0) 
        grid.addWidget(self.btn_add, 1, 0)
        grid.addWidget(self.btn_reset, 1, 1)             
        self.setLayout(grid)
    
    def record(self, ):
        self.count += 1
        logger.info(f"Click {self.count} times")

    def reset(self, ):
        self.count=0
        logger.error(f"Reset")


    @Slot(str, logging.LogRecord)
    def update_browser(self, status, record):
        (color, fontsize) = self.html_format.get(record.levelno, ("black", "12px"))
        s = '<pre><font color="%s" size="%s">%s</font></pre>' % (color, fontsize, status)
        # s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.browser.append(s)
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    layout=Layout()

    layout.show()
    app.exec_()