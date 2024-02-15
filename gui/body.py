from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class Body(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Основной макет
        self.main_layout = QVBoxLayout(self)

        # Макет для имени пользователя и профиля
        profile_layout = QHBoxLayout()
        self.text_edit = QTextEdit(self)
        profile_layout.addWidget(self.text_edit)

        # Виджет для профиля пользователя
        self._init_client_profile()
        profile_layout.addWidget(self.client_profile_widget, alignment=Qt.AlignRight)

        # Добавляем profile_layout в main_layout
        self.main_layout.addLayout(profile_layout)

        # Установка основного макета для виджета
        self.setLayout(self.main_layout)

    def _init_client_profile(self):
        self.client_profile_layout = QVBoxLayout()

        # Имя пользователя
        self.client_name_label = QLabel('Владимир', self)
        self.client_name_label.setFont(QFont('Arial', 20))
        self.client_profile_layout.addWidget(self.client_name_label, alignment=Qt.AlignLeft)

        # Аватар пользователя
        self.avatar_label = QLabel(self)
        self.avatar_pixmap = QPixmap()  # Путь к изображению аватара следует задать здесь
        self.avatar_label.setPixmap(self.avatar_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.client_profile_layout.addWidget(self.avatar_label)

        # ID пользователя
        self.client_id_label = QLabel('ID: 0', self)  # Пример ID
        self.client_id_label.setFont(QFont('Arial', 12))
        self.client_profile_layout.addWidget(self.client_id_label)

        # Дополнительная информация о пользователе
        is_loyal = False
        car = 'AUDI RS6'
        self.client_info_label = QLabel(f'Пр-ма лояльности: {is_loyal}\nМашина: {car}', self)
        self.client_info_label.setFont(QFont('Arial', 12))
        self.client_profile_layout.addWidget(self.client_info_label)

        # Контейнер для профиля
        self.client_profile_widget = QWidget()
        self.client_profile_widget.setLayout(self.client_profile_layout)

    def update_with_rabbit_message(self, rabbit_message):
        self.client_name_label.setText(rabbit_message.name)
        self.client_info_label.setText(
            f"Car Models: {rabbit_message.carModels}\n"
            f"Gas Station: {rabbit_message.gasStation}\n"
            f"Indexes: {rabbit_message.indexes}\n"
            f"Sails: {rabbit_message.sails}\n"
            f"Recommendations: {', '.join(rabbit_message.recommendations)}"
        )

    def update_client_profile(self, client_id, client_info, client_avatar_path):
        """Метод для обновления информации профиля пользователя."""
        self.client_id_label.setText(f'ID: {client_id}')
        self.client_info_label.setText(client_info)

        if client_avatar_path:
            new_avatar_pixmap = QPixmap(client_avatar_path)
            self.avatar_label.setPixmap(new_avatar_pixmap.scaled(100, 100, Qt.KeepAspectRatio))