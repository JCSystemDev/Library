from PySide6.QtWidgets import *
import loginwindow
from loginwindow import LoginWindow

if __name__ == "__main__":
    app = QApplication()
    app.setStyle("fusion")
    login_window: LoginWindow = loginwindow.LoginWindow()
    login_window.setFixedSize(login_window.size())
    login_window.show()
    app.exec()
