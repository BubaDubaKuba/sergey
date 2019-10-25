# TODO: add app icon

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFrame, QTextEdit, QPlainTextEdit, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QIcon, QColor, QTextCursor
from PyQt5.QtCore import QUrl, QRect, QPoint, QSize, Qt
#import PyQt5
import os
import random
import time
import threading
#import output

class SergeyBot:
    """Класс, отвечающий за "понимание" ввода пользователя.
    ("понимание" ввода пользователя можно было сделать с помощью
    функций, ну да ладна...)"""
    def __init__(self):
        self.is_answering = False
        self.quest_questions = ("")
        self.greeting_questions = ("привет", "здравствуй")
        self.all_questions = (self.quest_questions)
        self.default_answers = ("Непонял...", "Я играю в танки...")
    
    def answer(self, question : str):
        return random.choice(self.default_answers)

class Chat(QTextEdit):
    def __init__(self, str, parent=None):
        super().__init__(str, parent)
        self.setReadOnly(True)



class InputButton(QPushButton):
    def __init__(self, s, parent, mainApp):
        super().__init__(s, parent=parent)
        self.s = s
        self.mainApp = mainApp
        def clik():
            self.mainApp.inputbox.setText(self.s)
            self.mainApp.sendMsg()
        self.clicked.connect(clik)


class SergeyApp(QWidget):
    """Класс основного приложения.
    Тут располагаются все виджеты(кнопки, поля ввода и др.)"""
    def __init__(self):
        super().__init__()
        self.bot = SergeyBot()
        self.initUI()
    
    def sendMsg(self):
        txt = self.inputbox.text()
        self.inputbox.clear()
        if txt != "" and not self.bot.is_answering:
            self.chat.setTextColor(Qt.white)
            self.chat.append("Вы: " + txt)
            self.chat.setTextColor(Qt.black)
            self.chat.insertPlainText("\nСерёга: " + self.bot.answer(txt))
            """
            def async_answer():
                print("START_ASYNC")
                self.bot.is_answering = True
                # Анимация
                for i in range(3):
                    print("{")
                    self.chat.insertPlainText(".")
                    time.sleep(0.5)
                    print("}")
                self.bot.is_answering = False
                print("END_ASYNC")
            threading.Thread(target=async_answer).start()"""
            """# Очистить точки от анимации
            print("Fff")
            self.chat.setPlainText("")
            print('fgdfg')
            self.chat.insertPlainText(self.bot.answer(txt))
            self.bot.is_answering = False"""

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
        web = QWebEngineView(self)
        # Получаем абсолютный путь файла
        # map2.html (почему-то QWebEngineView
        # загружает только абсолютные пути файла).
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map2.html"))
        web.load(QUrl.fromLocalFile(file_path))

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

        self.chat = Chat("")
        
        
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
        main_layout.addWidget(web,          0, 60,  100, 40)

        #self.main_layout.setColumnStretch(0, 2)
        #self.main_layout.setColumnStretch(1, 1)

        #self.main_layout.setRowStretch(0, 3)
        #self.main_layout.setRowStretch(1, 1)


if __name__ == "__main__":
    import sys
    print("Start!")
    app = QApplication(sys.argv)
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
