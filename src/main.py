# TODO: add app icon

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QRect, QPoint, QSize, Qt
#import PyQt5
import os
import re

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
    

class SergeyApp(QWidget):
    """Класс основного приложения.
    Тут располагаются все виджеты(кнопки, поля ввода и др.)"""
    def __init__(self):
        super().__init__()
        self.showing_web = True
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
        self.web = QWebEngineView(self)
        # Получаем абсолютный путь файла
        # map2.html (почему-то QWebEngineView
        # загружает только абсолютные пути файла).
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map2.html"))
        self.web.load(QUrl.fromLocalFile(file_path))
        
        def btn_clicked():
            # Функция, которая вызывается при клике кнопки btn (пока для теста).
            if self.showing_web:
                # Функции
                # QWebEngineView.hide() и
                # QWebEngineView.show() "прячут" и показывают
                # окно страницы с картой соответственно.
                self.web.hide()
                self.showing_web = False
            else:
                self.web.show()
                self.showing_web = True
        # Инициализируем кнопку, с надписью "Butzon" на ней
        # и передаем наше основное окно(чтобы библиотека лучше понимала,
        # как рисовать кнопку).
        self.btn = QPushButton("Butzon", self)
        # Передаём ей функцию, которая вызывается при клике на кнопку.
        self.btn.clicked.connect(btn_clicked)

        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Box)
        self.frame.setStyleSheet("background-color: Gainsboro")
        self.lbl = QLabel("reerrer", self.frame)
        self.lbl.setWordWrap(True)
        
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
        self.main_layout = QGridLayout(self)
        # TODO: self.main_layout.setSpacing(10)
        # Добавляем все наши виджеты (кнопки, веб страницы и т.д.)
        self.main_layout.addWidget(self.btn, 0, 0, Qt.AlignLeft)
        self.main_layout.addWidget(self.frame, 1, 0)
        self.main_layout.addWidget(self.web, 0, 1, -1, -1)

        self.main_layout.setColumnStretch(0, 2)
        self.main_layout.setColumnStretch(1, 1)

        self.main_layout.setRowStretch(0, 3)
        self.main_layout.setRowStretch(1, 1)


if __name__ == "__main__":
    import sys
    print("Start!")
    help(SergeyApp.initUI)
    app = QApplication(sys.argv)
    sergey = SergeyApp()
    sergey.show()
    app.exec_()

    print("End!")
