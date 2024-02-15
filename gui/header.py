from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel


class Header(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addStretch()
        self.company_name_label = QLabel('TATNEFT')
        self.company_name_label.setFont(QFont('Arial', 18))
        self.company_name_label.setFixedHeight(30)
        self.addWidget(self.company_name_label, alignment=Qt.AlignLeft)

        self.date_time_label = QLabel()
        self.date_time_label.setFont(QFont('Arial', 16))
        self.date_time_label.setFixedHeight(30)
        self.addWidget(self.date_time_label, alignment=Qt.AlignRight)
        self.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss')
        self.date_time_label.setText(current_time)
