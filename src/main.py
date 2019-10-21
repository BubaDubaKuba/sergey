# TODO: add app icon

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QRect, QPoint, QSize
#import PyQt5
import os
import re

class SergeyBot:
    def __init__(self):
        self.quest_questions = ("")
        self.greeting_questions = ("привет", "здравствуй")
        self.all_questions = (self.quest_questions)
        self.default_answers = ("Непонял...", "Я играю в танки...")
    
    def answer(self, question : str):
        for question_type in self.all_questions:
            pass
    

class SergeyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.showing_web = True
        self.initUI()
    
    def initUI(self):
        self.showMaximized()
        self.setWindowTitle("SERGEY APP!!!")
        self.setWindowIcon(QIcon("icon.ico"))

        self.web = QWebEngineView(self)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map2.html"))
        self.web.load(QUrl.fromLocalFile(file_path))

        def btn_clicked():
            if self.showing_web:
                self.web.hide()
                self.showing_web = False
            else:
                self.web.show()
                self.showing_web = True
        self.btn = QPushButton("Butzon", self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(btn_clicked)

        self.lay = QGridLayout(self)
        self.lay.setSpacing(10)
        self.lay.addWidget(self.btn, 0, 0, 1, 1)
        self.lay.addWidget(self.web, 1, 2, 1, 2)

        self.lay.setColumnStretch(0, 2)
        self.lay.setColumnStretch(1, 1)
        self.lay.setColumnStretch(2, 2)
        


if __name__ == "__main__":
    import sys
    print("Start!")
    app = QApplication(sys.argv)
    sergey = SergeyApp()
    sergey.show()
    app.exec_()

    print("End!")
