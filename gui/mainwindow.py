import sys

from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QMainWindow, QLabel, QStatusBar, QApplication,
                             QGridLayout, QWidget, QVBoxLayout)
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QGridLayout, QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QTimer, QDateTime, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Установка размера окна
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('My Application')

        # Установка фона окна
        self.set_background()
        # Инициализация виджетов
        self.init_widgets()
        # Инициализация статусной строки
        self.init_status_bar()

    def init_status_bar(self):
        # Создание статусной строки
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово", 5000)

    def set_background(self):
        # Использование QLabel для установки фона
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        background_label = QLabel(self)
        background_pixmap = QPixmap('/path/to/your/image.png')  # Укажите правильный путь к вашему изображению
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)

        # Добавляем background_label в layout с координатами (0, 0)
        self.layout.addWidget(background_label, 0, 0, 1, 1)

    def init_widgets(self):
        # Основной виджет и главный макет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)  # Изменено на QVBoxLayout

        # Верхний макет для названия компании и даты/времени
        top_layout = QHBoxLayout()
        self.main_layout.addLayout(top_layout)

        # Название компании
        self.company_name_label = QLabel('TATNEFT', self)
        self.company_name_label.setFont(QFont('Arial', 24))
        top_layout.addWidget(self.company_name_label, alignment=Qt.AlignLeft)

        # Дата и время (выровнены по правому краю)
        self.date_time_label = QLabel(self)
        self.date_time_label.setFont(QFont('Arial', 16))
        top_layout.addWidget(self.date_time_label, alignment=Qt.AlignRight)

        # Макет для имени пользователя и профиля
        profile_layout = QHBoxLayout()
        self.main_layout.addLayout(profile_layout)

        # Имя пользователя
        self.client_name_label = QLabel('Владимир', self)
        self.client_name_label.setFont(QFont('Arial', 20))
        profile_layout.addWidget(self.client_name_label, alignment=Qt.AlignLeft)

        # Виджет для профиля пользователя
        self.init_client_profile()
        profile_layout.addWidget(self.client_profile_widget, alignment=Qt.AlignRight)

        # Таймер для обновления времени каждую секунду
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss')
        self.date_time_label.setText(current_time)

    def init_client_profile(self):
        self.client_profile_layout = QVBoxLayout()

        # Аватар пользователя
        self.avatar_label = QLabel(self)
        self.avatar_pixmap = QPixmap('')  # Укажите путь к изображению аватара
        self.avatar_label.setPixmap(self.avatar_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.client_profile_layout.addWidget(self.avatar_label)

        # ID пользователя
        self.client_id_label = QLabel(f'ID: {0}', self)     # set id
        self.client_id_label.setFont(QFont('Arial', 12))
        self.client_profile_layout.addWidget(self.client_id_label)

        # Дополнительная информация о пользователе
        is_loyal = False
        car = 'AUDI RS6'
        self.client_info_label = QLabel(f'Пр-ма лояльности: {is_loyal}\nМашина: {car}', self)   # is_loyal and car
        self.client_info_label.setFont(QFont('Arial', 12))
        self.client_profile_layout.addWidget(self.client_info_label)

        # Контейнер для профиля
        self.client_profile_widget = QWidget()
        self.client_profile_widget.setLayout(self.client_profile_layout)

    def update_client_profile(self, client_id, client_info, client_avatar_path):
        """Метод для обновления информации профиля пользователя."""
        # Обновление ID пользователя
        self.client_id_label.setText(f'ID: {client_id}')

        # Обновление информации о пользователе
        self.client_info_label.setText(client_info)

        # Обновление аватара пользователя, если предоставлен новый путь
        if client_avatar_path:
            new_avatar_pixmap = QPixmap(client_avatar_path)
            self.avatar_label.setPixmap(new_avatar_pixmap.scaled(100, 100, Qt.KeepAspectRatio))


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # run to test qt Application
    main()
