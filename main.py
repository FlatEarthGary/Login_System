from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

import pymongo

import sys
import time


class LoggedIn(QMainWindow):

    def __init__(self):
        
        super().__init__()

        print("Snälla")

        self.users = self.database_init()

        self.data = self.users.find({"username": "asd"})

        self.username = QtWidgets.QLineEdit("This should be read only")
        self.username.setReadOnly(True)

        self.name = QtWidgets.QLineEdit("This should be")
        self.name.setReadOnly(True)

        self.setFixedSize(500, 300)
        self.move(1000, 500)
        self.setWindowTitle("Logged in")

        layout = QtWidgets.QFormLayout()
        layout.addRow("Username:", self.username)
        layout.addRow("Name:", self.name)
        self.setLayout(layout)
        

    def database_init(self):
        
        self.client = pymongo.MongoClient()
        self.db = self.client.LoginSystem
        self.users = self.db.users

        return self.users

class loginWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.users = self.database_reinit()

        self.setWindowTitle("Login | FlatEarthGary")
        self.setFixedSize(500, 300)
        self.move(1000, 500)

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setFixedSize(200, 50)
        self.username.move(150, 65)

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setFixedSize(200, 50)
        self.password.move(150, 130)

        self.confirm = QtWidgets.QPushButton(self)
        self.confirm.setText("Confirm")
        self.confirm.setFixedSize(200, 50)
        self.confirm.move(150, 195)
        
        self.confirm.clicked.connect(self.login)
        



    def database_reinit(self):

        self.client = pymongo.MongoClient()
        self.db = self.client.LoginSystem
        self.users = self.db.users

        return self.users

    def login(self):
        
        if self.username.text() and self.password.text():

            if self.users.count_documents({"username": self.username.text().lower(), "password": self.password.text()}) == 1:
                self.logged_in = QtWidgets.QMessageBox()
                self.logged_in.setWindowTitle("Successfully Logged in")
                self.logged_in.setText("LOGGED In")
                self.logged_in.exec()
                main().check_logged_in_status()
                self.close()


            else:
                self.wrong = QtWidgets.QMessageBox()
                self.wrong.setWindowTitle("Error | Wrong login credentials | Error")
                self.wrong.setText("Either the username or password is incorrect, try again!")
                self.wrong.exec_()

    def test(self):
        print("This get")

            

    



class main(QMainWindow):

    def __init__(self, status=False):

        super().__init__()
        if not status:
            self.start_up()
    
    def start_up(self):
        self.registration_window = regWindow()
        self.login_window = loginWindow()
        self.loggedIn = LoggedIn()

        self.setFixedSize(500, 300)
        self.move(1000, 500)
        self.setWindowTitle("Secure login system | FlatEarthGary")

        self.layout = QVBoxLayout()

        self.login_button = QPushButton("Login")
        
        self.login_button.clicked.connect(self.check_login_status)

        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")

        self.register_button.clicked.connect(self.check_reg_status)

        self.layout.addWidget(self.register_button)

        win = QWidget()
        win.setLayout(self.layout)
        self.setCentralWidget(win)

        self.database_init()

    def database_init(self, want=False):

        self.client = pymongo.MongoClient()
        self.db = self.client.LoginSystem
        self.users = self.db.users

        return self.users

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()
        else:
            window.show()
    
    def check_reg_status(self):
        return self.toggle_window(self.registration_window)

    def check_login_status(self):
        return self.toggle_window(self.login_window)

    def check_logged_in_status(self):
        return self.toggle_window(self.loggedIn)
    


class regWindow(main):

    def __init__(self):
        super().__init__(status=True)
        self.setWindowTitle("Login system | Registration")
        self.setFixedSize(500, 300)
        self.move(1000, 500)

        self.label = QtWidgets.QLabel(self)
        
        self.username_label = QtWidgets.QLabel(self)
        self.username_label.setText("Username: ")
        self.username_label.move(50, 3)

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.move(130, 5)

        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setText("Password: ")
        self.password_label.move(50, 40)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.move(130, 40)

        self.first_name_label = QtWidgets.QLabel(self)
        self.first_name_label.setText("First name: ")
        self.first_name_label.move(50, 140)

        self.first_name_input = QtWidgets.QLineEdit(self)
        self.first_name_input.move(130, 140)

        self.last_name_label = QtWidgets.QLabel(self)
        self.last_name_label.setText("Last name: ")
        self.last_name_label.move(50, 175)

        self.last_name_input = QtWidgets.QLineEdit(self)
        self.last_name_input.move(130, 175)

        self.gender_label = QtWidgets.QLabel(self)
        self.gender_label.setText("Gender: ")
        self.gender_label.move(50, 210)

        self.gender = QtWidgets.QComboBox(self)
        self.gender.addItem("Male")
        self.gender.addItem("Female")
        self.gender.addItem("Other")
        self.gender.move(130, 210)

        self.mail_label = QtWidgets.QLabel(self)
        self.mail_label.setText("Mail adress: ")
        self.mail_label.move(50, 245)

        self.mail_input = QtWidgets.QLineEdit(self)
        self.mail_input.move(130, 245)

        # Confirm button
        self.confirm_button = QtWidgets.QPushButton("Confirm\n(this window will close automatically)", self)
        self.confirm_button.setFixedSize(250, 300)
        self.confirm_button.move(245, 0)
        self.confirm_button.clicked.connect(self.continue_button)

    def continue_button(self):
        print("Continue button")
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        self.first_name = self.first_name_input.text()
        self.last_name = self.last_name_input.text()

        if type(self.gender) != str:
            self.gender = self.gender.currentText()

        self.mail = self.mail_input.text()

        self.register_user = super().database_init()

        if self.register_user.count_documents({"username": self.username.lower()}) == 0:
            self.user = {"username": self.username.lower(), "password": self.password, "first_name": self.first_name.lower(), "last_name": self.last_name.lower(), "gender": self.gender, "mail": self.mail.lower()}
            self.users.insert_one(self.user)
            self.close()
        else:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error | Username already exists.")
            self.msg.setText("The username you have provided already exists. Please choose another one. ")
            self.msg.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = main()
    win.show()
    sys.exit(app.exec_())
