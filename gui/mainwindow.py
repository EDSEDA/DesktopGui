import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QStatusBar
from PyQt5.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Установка размера окна
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('My Application')

        # Установка фона окна
        self.set_background()
        # Добавление меток
        self.init_labels()
        # Добавление аватара и информации о пользователе
        self.init_client_profile()
        # Инициализация статусной строки
        self.init_status_bar()

    def init_status_bar(self):
        # Создание статусной строки
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Установка начального сообщения
        self.status_bar.showMessage("Готово", 5000)  # Отображение сообщения на 5 секунд

        # Можно использовать QTimer для периодического обновления статуса, если требуется
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(10000)  # Обновление каждые 10 секунд

    def update_status(self):
        # Метод для обновления информации статусной строки
        # Здесь вы можете добавить логику для проверки состояния подключения или других параметров
        self.status_bar.showMessage("Подключен", 5000)  # Пример сообщения

    def set_background(self):
        # Использование QLabel для установки фона
        background_label = QLabel(self)
        background_pixmap = QPixmap('/path/to/your/image.png')  # Укажите правильный путь к вашему изображению
        background_label.setPixmap(background_pixmap)
        background_label.resize(self.width(), self.height())  # Размер фона под размер окна
        background_label.setScaledContents(True)  # Масштабирует изображение по содержимому

        # Если вы хотите использовать цвет вместо изображения, раскомментируйте следующие строки:
        # color = QColor(255, 255, 255)  # Или любой цвет, который вы хотите
        # self.set_background_color(color)

    def set_background_color(self, color):
        # Установка цвета фона с использованием QPalette
        palette = self.palette()
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)

    def init_labels(self):
        # Название компании
        self.company_name_label = QLabel('TATNEFT', self)
        self.company_name_label.setFont(QFont('Arial', 24))
        self.company_name_label.move(150, 20)  # Позиционирование метки в окне

        # Дата и время
        self.date_time_label = QLabel(self)
        self.date_time_label.setFont(QFont('Arial', 16))
        self.date_time_label.move(150, 60)
        self.update_time()

        # Имя пользователя
        self.client_name_label = QLabel('Владимир', self)
        self.client_name_label.setFont(QFont('Arial', 20))
        self.client_name_label.move(150, 100)

        # Таймер для обновления времени каждую секунду
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        # Получение текущей даты и времени и установка в метку
        current_time = QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss')
        self.date_time_label.setText(current_time)

    def init_client_profile(self):
        # Создание виджета для профиля пользователя
        self.client_profile_widget = QWidget(self)
        self.client_profile_layout = QVBoxLayout(self.client_profile_widget)  # Вертикальное расположение

        # Метка для аватара
        self.avatar_label = QLabel(self)
        self.avatar_pixmap = QPixmap('/path/to/avatar/image.png')  # Укажите путь к изображению аватара
        self.avatar_label.setPixmap(self.avatar_pixmap.scaled(100, 100, Qt.KeepAspectRatio))

        # Метка для ID пользователя
        self.client_id_label = QLabel('ID: 2153546', self)
        self.client_id_label.setFont(QFont('Arial', 12))

        # Метка для дополнительной информации о пользователе
        self.client_info_label = QLabel('Пр-ма лояльности: есть\nМашина: AUDI RS6', self)
        self.client_info_label.setFont(QFont('Arial', 12))

        # Добавление меток в макет
        self.client_profile_layout.addWidget(self.avatar_label)
        self.client_profile_layout.addWidget(self.client_id_label)
        self.client_profile_layout.addWidget(self.client_info_label)

        # Установка позиции виджета профиля в окне
        self.client_profile_widget.setLayout(self.client_profile_layout)
        self.client_profile_widget.move(600, 20)  # Меняйте позицию в соответствии с вашим дизайном


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # run to test qt Application
    main()
