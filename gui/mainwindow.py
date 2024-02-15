import sys
from queue import Queue

from PyQt5.QtCore import QTimer, QDateTime, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QApplication, QMainWindow, QStatusBar, QTextEdit)

from rabbitmq_client.client import RabbitMQClient
from rabbitmq_client.schema import RabbitMessage
import json
from config import settings


class MainWindow(QMainWindow):
    message_signal = pyqtSignal(RabbitMessage)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_queue()

        # Установка размера окна
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('Recommendation system')
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.set_background()

        # Инициализация виджетов
        self.init_widgets()

    def set_background(self):
        # Использование QLabel для установки фона
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        background_label = QLabel(self)
        background_pixmap = QPixmap('resources/test_img/test_img.jpg')  # Укажите правильный путь к вашему изображению
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)

        # Добавляем background_label в layout с координатами (0, 0)
        self.layout.addWidget(background_label, 0, 0, 1, 1)

    def init_queue(self):
        self.queue = Queue()  # Очередь для коммуникации между RabbitMQ потоком и GUI потоком
        self.rabbitmq_client = RabbitMQClient(self.queue)  # Создаем экземпляр клиента RabbitMQ
        self.rabbitmq_client.start_consuming()  # Начинаем потребление сообщений
        self.message_signal.connect(self.update_text_edit)

    def init_status_bar(self):
        # Создание статусной строки
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово", 5000)

    def init_widgets(self):
        # Основной виджет и главный макет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self._init_header()
        self._init_body()
        self._init_footer()

    ##################################
    def _init_header(self):
        # Верхний макет для названия компании и даты/времени
        top_layout = QHBoxLayout()
        self.main_layout.addLayout(top_layout)

        top_layout.addStretch()
        # Название компании
        self.company_name_label = QLabel('TATNEFT', self)
        self.company_name_label.setFont(QFont('Arial', 18))
        self.company_name_label.setFixedHeight(30)
        top_layout.addWidget(self.company_name_label, alignment=Qt.AlignLeft)

        # Дата и время (выровнены по правому краю)
        self.date_time_label = QLabel(self)
        self.date_time_label.setFont(QFont('Arial', 16))
        self.date_time_label.setFixedHeight(30)
        top_layout.addWidget(self.date_time_label, alignment=Qt.AlignRight)
        top_layout.addStretch()
        # Таймер для обновления времени каждую секунду
        self._init_timer()

    def _init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)

    def _update_time(self):
        current_time = QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss')
        self.date_time_label.setText(current_time)

    ##################################
    def _init_body(self):
        # Макет для имени пользователя и профиля
        profile_layout = QHBoxLayout()
        self.main_layout.addLayout(profile_layout)

        # Виджет для профиля пользователя
        self._init_client_profile()
        profile_layout.addWidget(self.client_profile_widget, alignment=Qt.AlignRight)

    def _init_client_profile(self):
        self.client_profile_layout = QVBoxLayout()

        # Имя пользователя
        self.client_name_label = QLabel('Владимир', self)
        self.client_name_label.setFont(QFont('Arial', 20))
        self.client_profile_layout.addWidget(self.client_name_label, alignment=Qt.AlignLeft)

        # Аватар пользователя
        self.avatar_label = QLabel(self)
        self.avatar_pixmap = QPixmap('')  # Укажите путь к изображению аватара
        self.avatar_label.setPixmap(self.avatar_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.client_profile_layout.addWidget(self.avatar_label)

        # ID пользователя
        self.client_id_label = QLabel(f'ID: {0}', self)  # set id
        self.client_id_label.setFont(QFont('Arial', 12))
        self.client_profile_layout.addWidget(self.client_id_label)

        # Дополнительная информация о пользователе
        is_loyal = False
        car = 'AUDI RS6'
        self.client_info_label = QLabel(f'Пр-ма лояльности: {is_loyal}\nМашина: {car}', self)  # is_loyal and car
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

    ##################################
    def _init_footer(self):
        ...

    ##################################

    def update_text_edit(self, rabbit_message):
        # Обновляем виджет текстовым сообщением
        # Используем данные из модели RabbitMessage
        message_text = (
            f"Name: {rabbit_message.name}\n"
            f"Car Models: {rabbit_message.carModels}\n"
            f"Gas Station: {rabbit_message.gasStation}\n"
            f"Indexes: {rabbit_message.indexes}\n"
            f"Sails: {rabbit_message.sails}\n"
            f"Recommendations: {', '.join(rabbit_message.recomendations)}"
        )
        self.text_edit.append(message_text)
    def start(self):
        # Запускаем поток для проверки наличия новых сообщений в queue
        self.thread = QThread()  # Создаем QThread
        self.thread.started.connect(self.check_queue)
        self.thread.start()

    def check_queue(self):
        while True:
            if not self.queue.empty():
                message_body = self.queue.get()
                try:
                    # Преобразование байтов в строку и десериализация JSON в экземпляр RabbitMessage
                    message_data = json.loads(message_body.decode('utf-8'))
                    rabbit_message = RabbitMessage(**message_data)
                    self.message_signal.emit(rabbit_message)  # Отправляем экземпляр в GUI поток
                except Exception as e:
                    print(f"Error processing message: {e}")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # run to test qt Application
    main()
