import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidgetItem, QListWidget, \
    QTableWidgetItem, QTableWidget, QHeaderView
from config import CLIENT_AVATAR_PATH


class Body(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Основной макет
        self.main_layout = QVBoxLayout(self)

        # Макет для имени пользователя и профиля
        client_layout = QVBoxLayout()

        # Виджет для профиля пользователя
        self._init_client_profile()
        client_layout.addWidget(self.client_profile_widget)  # alignment=Qt.AlignRight
        self._init_client_recommendations()
        client_layout.addWidget(self.client_recommendations_widget, )  # alignment=Qt.AlignRight

        # Добавляем client_layout в main_layout
        self.main_layout.addLayout(client_layout)

        # Установка основного макета для виджета
        self.setLayout(self.main_layout)

    def _init_client_recommendations(self):
        self.client_recommendation_layout = QVBoxLayout()

        # Надпись "Специально для Вас"
        special_label = QLabel("Специально для Вас:", self)
        special_label.setFont(QFont('Montserrat', 16))
        special_label.setStyleSheet("font-weight: bold;")

        # Таблица рекомендаций
        self.client_recommendation_table = QTableWidget(self)
        self.client_recommendation_table.setFont(QFont('Montserrat', 12))  # Использование шрифта Montserrat
        self.client_recommendation_table.setStyleSheet("background-color: white;")  # Белый фон для таблицы

        # Устанавливаем количество строк и колонок
        self.client_recommendation_table.setRowCount(5)  # Пример для 5 рекомендаций
        self.client_recommendation_table.setColumnCount(2)  # Две колонки: имя товара и скидка на товар

        # Устанавливаем заголовки для колонок
        self.client_recommendation_table.setHorizontalHeaderLabels(['Имя товара', 'Скидка на товар'])

        # Заполняем таблицу данными (пример)
        for i in range(5):
            self.client_recommendation_table.setItem(i, 0, QTableWidgetItem(f'Товар {i + 1}'))
            self.client_recommendation_table.setItem(i, 1, QTableWidgetItem(f'{i * 10}%'))  # Пример скидки

        # Разрешаем выделение строк
        self.client_recommendation_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Делаем колонки растягивающимися на всю ширину виджета
        self.client_recommendation_table.horizontalHeader().setStretchLastSection(True)
        self.client_recommendation_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Добавляем таблицу в компоновку
        self.client_recommendation_layout.addWidget(special_label, alignment=Qt.AlignLeft)
        self.client_recommendation_layout.addWidget(self.client_recommendation_table)

        # Контейнер для рекомендаций
        self.client_recommendations_widget = QWidget()
        self.client_recommendations_widget.setLayout(self.client_recommendation_layout)
        # self.client_recommendation_layout = QVBoxLayout()
        #
        # # Надпись "Специально для Вас"
        # special_label = QLabel("Специально для Вас:", self)
        # special_label.setFont(QFont('Montserrat', 16))
        # special_label.setStyleSheet("font-weight: bold;")
        #
        # # Список Рекомендаций
        # self.client_recommendation_list = QListWidget(self)
        # self.client_recommendation_list.setFont(QFont('Montserrat', 12))  # Использование шрифта Montserrat
        # self.client_recommendation_list.setStyleSheet("background-color: white;")  # Белый фон для списка
        #
        # # Добавление примерных рекомендаций
        # for i in range(5):  # Пример добавления 5 рекомендаций
        #     item_text = f"Рекомендация {i + 1}: ..."
        #     item = QListWidgetItem(item_text)
        #     # Установка размера элемента списка, если необходимо
        #     # item.setSizeHint(QSize(-1, 50))
        #     self.client_recommendation_list.addItem(item)
        #
        # self.client_recommendation_layout.addWidget(special_label, alignment=Qt.AlignLeft)
        # self.client_recommendation_layout.addWidget(self.client_recommendation_list)
        #
        # # Контейнер для профиля
        # self.client_recommendations_widget = QWidget()
        # self.client_recommendations_widget.setLayout(self.client_recommendation_layout)

    def _init_client_profile(self):
        self.client_profile_layout = QHBoxLayout()

        # Аватар пользователя
        self.avatar_label = QLabel(self)
        self.avatar_pixmap = QPixmap(f'{CLIENT_AVATAR_PATH}/base_client_img.png')  # Путь к изображению аватара
        self.avatar_label.setPixmap(self.avatar_pixmap.scaled(250, 250, Qt.KeepAspectRatio))
        self.client_profile_layout.addWidget(self.avatar_label, alignment=Qt.AlignTop)

        # Горизонтальная компоновка для имени и информации пользователя
        info_layout = QVBoxLayout()

        self.client_name_label = QLabel('Имя клиента', self)
        self.client_name_label.setFont(QFont('Montserrat', 20))
        info_layout.addWidget(self.client_name_label, alignment=Qt.AlignTop)

        self.client_info_label = QLabel('''Модель машины: X\nНомер колонки: X\nИдентификатор: X''', self)
        self.client_info_label.setFont(QFont('Montserrat', 12))
        # self.client_info_label.setStyleSheet("border: 1px solid black; padding: 5px;")
        info_layout.addWidget(self.client_info_label, alignment=Qt.AlignTop)
        # Установка интервала между элементами компоновки

        self.client_profile_layout.addLayout(info_layout)

        # Контейнер для профиля
        self.client_profile_widget = QWidget()
        self.client_profile_widget.setLayout(self.client_profile_layout)

    def update_with_rabbit_message(self, rabbit_message):
        self.client_name_label.setText(rabbit_message.name)

        # Очистить текущую таблицу рекомендаций
        self.client_recommendation_table.setRowCount(0)

        # Рекомендации в таблицу
        for i, recommendation in enumerate(rabbit_message.recommendations):
            # Добавление новой строки в таблицу на каждой итерации
            row_position = self.client_recommendation_table.rowCount()
            self.client_recommendation_table.insertRow(row_position)

            # Случайная скидка из списка [0, 10, 20, 30, 40]
            discount = random.choice([0, 10, 20, 30, 40])

            # Заполнение данных о товаре и скидке
            self.client_recommendation_table.setItem(row_position, 0, QTableWidgetItem(recommendation))
            self.client_recommendation_table.setItem(row_position, 1, QTableWidgetItem(f"{discount}%"))

        # Обновить аватар пользователя
        new_avatar_pixmap = QPixmap(f'{CLIENT_AVATAR_PATH}/{rabbit_message.name}.jpg')
        self.avatar_label.setPixmap(new_avatar_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
