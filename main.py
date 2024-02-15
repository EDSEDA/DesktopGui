import sys

from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow


def start_QApp():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.start()
    sys.exit(app.exec_())


def main():
    start_QApp()


if __name__ == "__main__":
    main()
