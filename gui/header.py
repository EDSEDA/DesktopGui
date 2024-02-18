from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel


class Header(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addStretch()

        self.date_time_label = QLabel()
        self.date_time_label.setFont(QFont('Montserrat', 14))
        self.date_time_label.setFixedHeight(30)
        self.addWidget(self.date_time_label, alignment=Qt.AlignRight)
        self.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss')
        self.date_time_label.setText(current_time)
