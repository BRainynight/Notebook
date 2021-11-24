import logging, sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot

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

if __name__=="__main__":
    class GUI:
        def __init__(self) -> None:
            h = QtHandler(self.update_browser)
            self.handler = h
            h.setFormatter(logging.Formatter('%(message)s'))
            h.setLevel(logging.DEBUG)