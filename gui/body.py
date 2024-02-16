from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit
from config import CLIENT_AVATAR_PATH


class Body(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Основной макет
        self.main_layout = QVBoxLayout(self)

        # Макет для имени пользователя и профиля
        client_layout = QHBoxLayout()

        # Виджет для профиля пользователя
        self._init_client_profile()
        client_layout.addWidget(self.client_profile_widget, )  # alignment=Qt.AlignRight
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
        special_label.setFont(QFont('Arial', 12))
        special_label.setStyleSheet("font-weight: bold;")

        # Рекомендации
        self.client_recommendation_label = QLabel(f'Рекомендации: ...', self)
        self.client_recommendation_label.setFont(QFont('Arial', 12))
        self.client_recommendation_label.setStyleSheet("border: 1px solid black; padding: 5px;")

        self.client_recommendation_layout.addWidget(special_label, alignment=Qt.AlignLeft)
        self.client_recommendation_layout.addWidget(self.client_recommendation_label)

        # Контейнер для профиля
        self.client_recommendations_widget = QWidget()
        self.client_recommendations_widget.setLayout(self.client_recommendation_layout)

    def _init_client_profile(self):
        self.client_profile_layout = QVBoxLayout()

        # Имя пользователя
        self.client_name_label = QLabel('NoName', self)
        self.client_name_label.setFont(QFont('Arial', 20))
        self.client_profile_layout.addWidget(self.client_name_label, alignment=Qt.AlignLeft)

        # Аватар пользователя
        self.avatar_label = QLabel(self)
        self.avatar_pixmap = QPixmap(f'{CLIENT_AVATAR_PATH}/base_client_img.png')  # Путь к изображению аватара следует задать здесь
        self.avatar_label.setPixmap(self.avatar_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        # self.avatar_label.setPixmap(self.avatar_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.client_profile_layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)

        # Дополнительная информация о пользователе
        self.client_info_label = QLabel(f'О пользователе: ...', self)
        self.client_info_label.setFont(QFont('Arial', 12))
        self.client_info_label.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.client_profile_layout.addWidget(self.client_info_label)

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
        self.client_recommendation_label.setText(
            f"Скидка: {rabbit_message.sails}\n"
            f"Рекомендации: {', '.join(rabbit_message.recommendations)}"
        )

        new_avatar_pixmap = QPixmap(f'{CLIENT_AVATAR_PATH}/{rabbit_message.name}.jpg')
        self.avatar_label.setPixmap(new_avatar_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
