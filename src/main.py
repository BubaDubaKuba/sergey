# TODO: add app icon

import PySide2

from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFrame, QTextEdit, QPlainTextEdit, QLineEdit, QSpacerItem, QSizePolicy
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtGui import QIcon, QColor, QTextCursor
from PySide2.QtCore import QObject, Slot, QUrl, QRect, QPoint, QSize, Qt, QCoreApplication, QFile, QTextStream
#import PyQt5
import os
import random
import json
import time
import threading
import re
#import output

# вычисляет аа
def distance(p1, p2):
    pass

def isStrInList(s, l):
    #print("is", s, "in", l, "?")
    for i in l:
        if i in s:
            return True
    return False


class CallHandler(QObject):
    """Принимает вызовы из джаваскрипта"""
    @Slot(int)
    def test(self, nodeId):
        print('CALCAL Call received', nodeId)

class SergeyBot:
    """Класс, отвечающий за "понимание" ввода пользователя.
    ("понимание" ввода пользователя можно было сделать с помощью
    функций, ну да ладна...)"""
    def __init__(self, app):
        self.is_answering = False
        self.waiting_for_destination = False
        self.app = app
        self.quest = app.quest
        self.traverse_root = None
        self.prev_coords = None
        self.quest_questions = ("квест", "приключение", "хачю гулять")
        self.greeting_questions = ("привет", "здравствуй")
        self.greeting_answers = ("Привет!", "Здравствуй!")
        self.default_answers = ("Непонял...", "Я играю в танки...")
    
    def printToChat(self, s : str):
        self.app.chat.insertPlainText(s)
        self.app.chat.verticalScrollBar().setValue(self.app.chat.verticalScrollBar().maximum())
    
    def printPossibleDestinations(self):
        self.printToChat("Куда пойдём?\n")
        places = self.traverse_root["nodes"]
        for i in range(len(places) - 1):
            self.printToChat("В \"" + places[i]["name"] + "\" или\n")
        self.printToChat("В \"" + places[-1]["name"] + "\"")

    def answer(self, question : str):
        question = question.lower()
        if self.waiting_for_destination:
            destination = None
            destination_index = 0
            for i in range(len(self.traverse_root["nodes"])):
                if question == self.traverse_root["nodes"][i]["name"].lower():
                    destination = question
                    destination_index = i
                    break
            
            if destination != None:
                self.waiting_for_destination = False
                self.traverse_root = self.traverse_root["nodes"][destination_index]
                print(self.traverse_root)
                self.printToChat(self.traverse_root["description"])
            else:
                self.printPossibleDestinations()
        elif isStrInList(question, self.quest_questions):
            self.app.web.page().runJavaScript("""map.flyTo({center: [
				                            -74.50 + (Math.random() - 0.5) * 10,
				                            40 + (Math.random() - 0.5) * 10]})""")
            self.printToChat("Загружаю квест...\n")
            self.printToChat(self.quest["quest_name"] + ".\n" + self.quest["quest_description"] + "\n")
            self.traverse_root = self.quest["quest_tree"]
            self.printPossibleDestinations()
            self.waiting_for_destination = True
        elif isStrInList(question, self.greeting_questions):
            self.printToChat(random.choice(self.greeting_answers))
        
        else:
            self.printToChat(random.choice(self.default_answers))

class Chat(QTextEdit):
    def __init__(self, str = "", parent=None):
        super().__init__(str, parent)
        self.setReadOnly(True)
        #with f = open("chat.html")

class InputButton(QPushButton):
    def __init__(self, s, parent, mainApp):
        super().__init__(s, parent=parent)
        self.s = s
        self.mainApp = mainApp
        def clik():
            self.mainApp.inputbox.setText(self.s)
            self.mainApp.sendMsg()
        self.clicked.connect(clik)

class WebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print("javaScriptConsoleMessage: ", level, "[\"", message, "\"]", lineNumber, sourceID)

class SergeyApp(QWidget):
    """Класс основного приложения.
    Тут располагаются все виджеты(кнопки, поля ввода и др.)"""
    def __init__(self):
        super().__init__()
        with open("src/quest.json", encoding="utf-8") as f:
            self.quest = json.load(f)
        self.bot = SergeyBot(self)

        self.initUI()
    
    def sendMsg(self):
        txt = self.inputbox.text()
        self.inputbox.clear()
        if txt != "" and not self.bot.is_answering:
            self.bot.is_answering = True
            self.chat.setTextColor(Qt.white)
            self.chat.append("Вы: " + txt)
            self.chat.setTextColor(Qt.black)
            self.chat.insertPlainText("\nСерёга: ")
            self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())

            for i in range(3):
                self.chat.insertPlainText(".")
                # Чтобы отображалась "анимация" точек,
                # нужно каждый раз говорить приложению обновиться
                QCoreApplication.processEvents()
                time.sleep(0.5)
            for i in range(3):
                self.chat.textCursor().deletePreviousChar()
            self.bot.answer(txt)
            self.bot.is_answering = False

    def initUI(self):
        """Функция инициализации всех виджетов
        (вызывать её не надо)"""


        # showMaximized() изменяет размер окна на максимальный.
        self.showMaximized()
        # Присваиваем названию окна строку "SERGEY APP!!!".
        self.setWindowTitle("SERGEY APP!!!")
        # Должно менять иконку приложения (Почему-то не работает).
        self.setWindowIcon(QIcon("icon.ico"))

        

        # QWebEngineView - класс библиотеки, с помощью которого можно
        # отображать Web страницы (сайты из интернета или
        # просто локальные файлы HTML).
        # Иницилиализируем его, передавая обьект нашего главного класса.
        self.web = QWebEngineView(self)
        # Получаем абсолютный путь файла
        # map2.html (почему-то QWebEngineView
        # загружает только абсолютные пути файла).
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
        self.web.setPage(WebPage(self.web))
        self.web.load(QUrl.fromLocalFile(file_path))
        
        def ready(retVal):
            print("Returned:", retVal)
        def loadFinished(ok):
            if ok:
                #self.web.page().runJavaScript("bruhmoment()", ready)
                pass
        self.web.loadFinished.connect(loadFinished)

        self.jsChannel = QWebChannel()
        self.jsHandler = CallHandler()
        self.jsChannel.registerObject("jsHandler", self.jsHandler)
        self.web.page().setWebChannel(self.jsChannel)

        input_frame = QFrame(self)
        input_frame.setFrameStyle(QFrame.Box)

        inputgrid = QGridLayout(input_frame)
        
        inputButtonTexts = ["Привет!", "Квест", "Пока!"]
        buttons = []
        for i in range(len(inputButtonTexts)):
            buttons.append(InputButton(inputButtonTexts[i], input_frame, self))
            inputgrid.addWidget(buttons[i], 0, i, 1, 1)
        
        self.inputbox = QLineEdit(input_frame)
        self.inputbox.returnPressed.connect(self.sendMsg)
        inputgrid.addWidget(self.inputbox, 1, 0, 1, -1)

        self.chat = Chat()
        
        # QGridLayout - один из макетных классов, которые помогает управлять
        # положением виджетов. Этот класс управляет положениями виджетов
        # с помощью "таблицы", например как в Excel.
        # Виджеты могут занимать несколько "клеток" в таблице.
        # Пример макета:
        # +------------+----------------+
        # |   Кнопка   |                |
        # +------------+  Что-то еще... |
        # |            |                |
        # | Поле ввода +----------------+
        # |            | Какой-то текст |
        # +------------+----------------+
        main_layout = QGridLayout(self)


        # Добавляем все наши виджеты (кнопки, веб страницы и т.д.)
        main_layout.addWidget(self.chat,   0, 0,  80, 60)
        main_layout.addWidget(input_frame,  80, 0,  20, 60)
        main_layout.addWidget(self.web,          0, 60,  100, 40)

        #self.main_layout.setColumnStretch(0, 2)
        #self.main_layout.setColumnStretch(1, 1)

        #self.main_layout.setRowStretch(0, 3)
        #self.main_layout.setRowStretch(1, 1)


if __name__ == "__main__":
    import sys
    print("Start!")
    app = QApplication(sys.argv)
    #pyqt = os.path.dirname(PySide2.__file__)
    #QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))
    app.setStyleSheet("""
        QFrame {
            border: 0;
            background-color: Gainsboro;
            margin: 10px;
        }
        QLabel {
            background-color: LightGray;
            padding: 15px;
            font-size: 15pt;
            qproperty-alignment: AlignLeft;
            margin: 10px;
        }
        Chat {
            background-color: LightGray;
            padding: 15px;
            font-size: 15pt;
            margin: 10px;
        }
        QLineEdit {
            background-color: Silver;
            font-size: 15pt;
        }
        InputButton {
            background-color: ForestGreen;
            color: White;
            font-weight: Bold;
            border-radius: 5px;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: Green;
        }
        QPushButton:pressed {
            background-color: DarkGreen;
        }
        QWebEngineView {
            margin: 10px;
        }
    """)
    sergey = SergeyApp()
    sergey.show()
    app.exec_()

    print("End!")
