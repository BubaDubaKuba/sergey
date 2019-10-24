# TODO: add app icon

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QTextEdit, QPlainTextEdit, QSpacerItem
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QRect, QPoint, QSize, Qt
#import PyQt5
import os
import re
#import output

class SergeyBot:
    """Класс, отвечающий за "понимание" ввода пользователя.
    ("понимание" ввода пользователя можно было сделать с помощью
    функций, ну да ладна...)"""
    def __init__(self):
        self.quest_questions = ("")
        self.greeting_questions = ("привет", "здравствуй")
        self.all_questions = (self.quest_questions)
        self.default_answers = ("Непонял...", "Я играю в танки...")
    
    def answer(self, question : str):
        for question_type in self.all_questions:
            pass
    

class InputButton(QPushButton):
    def __init__(self, str, parent=None):
        super().__init__(str, parent=parent)
        self.clicked.connect(lambda: print(self.text()))


class SergeyApp(QWidget):
    """Класс основного приложения.
    Тут располагаются все виджеты(кнопки, поля ввода и др.)"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
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

        frame = QFrame(self)
        frame.setFrameStyle(QFrame.Box)

        inputgrid = QGridLayout(frame)
        
        inputButtonTexts = ["Butzon", "Futzon", "Kutson"]
        buttons = []
        for i in range(len(inputButtonTexts)):
            buttons.append(InputButton(inputButtonTexts[i], frame))
            inputgrid.addWidget(buttons[i], 0, i, 1, 1)
        self.inputbox = QPlainTextEdit("", frame)
        inputgrid.addWidget(self.inputbox, 1, 0, 1, len(buttons))
        self.inputbox.setPlainText("")

        lbl = QLabel("reerrer", self)
        lbl.setWordWrap(True)
        
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
        main_layout.addWidget(lbl,   0,  0,   70,   60)
        main_layout.addWidget(frame, 70, 0,   30,   60)
        main_layout.addWidget(web,   0,  60,  100,  40)

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
        QPlainTextEdit {
            background-color: White;
            font-size: 15pt;
        }
        QPushButton {
            background-color: Green;
            color: White;
            font-weight: Bold;
            min-height: 20px;
        }
        QWebEngineView {
            margin: 10px;
        }
    """)
    sergey = SergeyApp()
    sergey.show()
    app.exec_()

    print("End!")
