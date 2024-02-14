from PyQt5.QtWidgets import QApplication
from gui.mainwindow import MainWindow
import sys
import sys
import threading


def console_listener(window):
    while True:
        user_input = input("Введите '1' для обновления профиля: ")
        if user_input == '1':
            # Обновите это соответствующими данными
            new_id = '123456789'
            new_info = 'Новая информация\nНовые данные'
            new_avatar_path = 'resources/test_img/test_img.jpg'
            # Используйте методы Qt для обновления GUI из основного потока
            window.update_client_profile(new_id, new_info, new_avatar_path)


def start_QApp():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    # Запуск слушателя консоли в отдельном потоке
    threading.Thread(target=console_listener, args=(main_window,), daemon=True).start()
    sys.exit(app.exec_())


def main():
    start_QApp()


if __name__ == "__main__":
    main()
