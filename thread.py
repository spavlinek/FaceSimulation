from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
import sys,threading
def window():
    app = QApplication(sys.argv)
    window = QWidget()
    btn = QPushButton()
    btn.setText("Input In Console")
    box = QFormLayout()
    box.addRow(btn)
    btn.clicked.connect(input_txt)
    window.setLayout(box)
    window.show()
    sys.exit(app.exec_())

def input_txt():
    thread = threading.Thread(target=input)
    thread.start()

if __name__ == "__main__":
    window()