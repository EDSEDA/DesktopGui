import json
import sys
from queue import Queue

from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget,
                             QApplication, QMainWindow, QGridLayout)

from gui.body import Body
from gui.header import Header
from rabbitmq_client.client import RabbitMQClient
from rabbitmq_client.schema import RabbitMessage


class Worker(QRunnable):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)


class MainWindow(QMainWindow):
    message_signal = pyqtSignal(RabbitMessage)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_queue()

        # Установка размера окна
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('Recommendation system')

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

    def init_widgets(self):
        # Основной виджет и главный макет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.header = Header()
        self.main_layout.addLayout(self.header)
        self.body = Body()
        self.main_layout.addWidget(self.body)

    def update_text_edit(self, rabbit_message):
        self.body.update_with_rabbit_message(rabbit_message)

    def start(self):
        # Создаем рабочего и передаем в него функцию для выполнения
        self.worker = Worker(self.check_queue)
        # Запускаем рабочего в пуле потоков
        QThreadPool.globalInstance().start(self.worker)

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
    main_window.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # run to test qt Application
    main()
