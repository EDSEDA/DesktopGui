from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidgetItem, QListWidget
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

        # Список Рекомендаций
        self.client_recommendation_list = QListWidget(self)
        self.client_recommendation_list.setFont(QFont('Montserrat', 12))  # Использование шрифта Montserrat
        self.client_recommendation_list.setStyleSheet("background-color: white;")  # Белый фон для списка

        # Добавление примерных рекомендаций
        for i in range(5):  # Пример добавления 5 рекомендаций
            item_text = f"Рекомендация {i + 1}: ..."
            item = QListWidgetItem(item_text)
            # Установка размера элемента списка, если необходимо
            # item.setSizeHint(QSize(-1, 50))
            self.client_recommendation_list.addItem(item)

        self.client_recommendation_layout.addWidget(special_label, alignment=Qt.AlignLeft)
        self.client_recommendation_layout.addWidget(self.client_recommendation_list)

        # Контейнер для профиля
        self.client_recommendations_widget = QWidget()
        self.client_recommendations_widget.setLayout(self.client_recommendation_layout)

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
        self.client_info_label.setText(
            f"Модель машины: {rabbit_message.carModels}\n"
            f"Номер колонки: {rabbit_message.gasStation}\n"
            f"Идентификатор: {rabbit_message.indexes}\n"
        )
        self.client_recommendation_list.clear()

        # Рекомендации в список
        for recommendation in rabbit_message.recommendations:
            item = QListWidgetItem(f"Скидка: {rabbit_message.sails} - Рекомендация: {recommendation}")
            self.client_recommendation_list.addItem(item)

        new_avatar_pixmap = QPixmap(f'{CLIENT_AVATAR_PATH}/{rabbit_message.name}.jpg')
        self.avatar_label.setPixmap(new_avatar_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
