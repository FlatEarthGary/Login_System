from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

import sys

import pymongo

class registration(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Secure Login System | Registration | FlatEarthGary")
        self.setFixedSize(500, 300)
        self.move(1000, 500)
        
        self.username_label = QtWidgets.QLabel(self)
        self.username_label.setText("Username: ")
        self.username_label.move(68, 13)

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setFixedSize(100, 30)
        self.username_input.move(130, 5)

        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setText("Password: ")
        self.password_label.move(68, 48)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setFixedSize(100, 30)
        self.password_input.move(130, 40)

        self.first_name_label = QtWidgets.QLabel(self)
        self.first_name_label.setText("First name: ")
        self.first_name_label.move(57, 148)

        self.first_name_input = QtWidgets.QLineEdit(self)
        self.first_name_input.setFixedSize(100, 30)
        self.first_name_input.move(130, 140)

        self.last_name_label = QtWidgets.QLabel(self)
        self.last_name_label.setText("Last name: ")
        self.last_name_label.move(62, 183)

        self.last_name_input = QtWidgets.QLineEdit(self)
        self.last_name_input.setFixedSize(100, 30)
        self.last_name_input.move(130, 175)

        self.gender_label = QtWidgets.QLabel(self)
        self.gender_label.setText("Gender: ")
        self.gender_label.move(80, 218)

        self.gender = QtWidgets.QComboBox(self)
        self.gender.addItem("Male")
        self.gender.addItem("Female")
        self.gender.addItem("Other")
        self.gender.move(130, 210)

        self.mail_label = QtWidgets.QLabel(self)
        self.mail_label.setText("Mail adress: ")
        self.mail_label.move(50, 253)

        self.mail_input = QtWidgets.QLineEdit(self)
        self.mail_input.setFixedSize(100, 30)
        self.mail_input.move(130, 245)

        # Confirm button
        self.confirm_button = QtWidgets.QPushButton("Confirm\n(this window will close automatically)", self)
        self.confirm_button.setFixedSize(250, 300)
        self.confirm_button.move(245, 0)
        self.confirm_button.clicked.connect(self.continue_button)

    def continue_button(self):

        self.username = self.username_input.text()
        self.password = self.password_input.text()
        self.first_name = self.first_name_input.text()
        self.last_name = self.last_name_input.text()
        self.mail = self.mail_input.text()

        if self.username and self.password and self.first_name and self.last_name and self.mail and self.gender:
    
            if type(self.gender) != str:
                self.gender = self.gender.currentText()

            self.database = Main().database()

            if self.database.count_documents({"username_lower": self.username.lower()}) == 0:
                
                self.user = {"username": self.username, "password": self.password, "first_name": self.first_name, "last_name": self.last_name, "gender": self.gender, "mail": self.mail, "username_lower": self.username.lower()}
                
                self.database.insert_one(self.user)
                self.hide()
            else:
                self.msg = QtWidgets.QMessageBox(self)
                self.msg.setWindowTitle("Username already exists")
                self.msg.setText("The username (%s) is unfortunately already taken, try again!" % (self.username))
                self.msg.exec_()

class loggedIn(QWidget):

    def __init__(self, username):

        super().__init__()

        self.username = username

        self.setWindowTitle("Secure Login System | Logged In | FlatEarthGary")
        self.setFixedSize(500, 300)
        self.move(1000, 500)

        self.database = Main().database()

        self.data = self.database.find({"username_lower": self.username})[0]

        self.username_field = QtWidgets.QLineEdit(self.data["username"])
        self.username_field.setReadOnly(True)

        self.first_name = QtWidgets.QLineEdit(self.data["first_name"].lower().capitalize())
        self.first_name.setReadOnly(True)

        self.last_name = QtWidgets.QLineEdit(self.data["last_name"].capitalize())
        self.last_name.setReadOnly(True)

        self.gender = QtWidgets.QLineEdit(self.data["gender"].capitalize())
        self.gender.setReadOnly(True)

        self.mail = QtWidgets.QLineEdit(self.data["mail"])
        self.mail.setReadOnly(True)

        self.setFixedSize(500, 300)
        self.move(1000, 500)
        self.setWindowTitle("Logged in")

        layout = QtWidgets.QFormLayout()
        layout.addRow("Username:", self.username_field)
        layout.addRow("Name:", self.first_name)
        layout.addRow("Last name:", self.last_name)
        layout.addRow("Gender:", self.gender)
        layout.addRow("Mail adress:", self.mail)
        self.setLayout(layout)




class login(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Secure Login System | Login | FlatEarthGary")
        self.setFixedSize(500, 300)
        self.move(1000, 500)

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setFixedSize(200, 50)
        self.username.move(150, 65)

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setFixedSize(200, 50)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.move(150, 130)

        self.confirm_button = QtWidgets.QPushButton(self)
        self.confirm_button.setText("Confirm")
        self.confirm_button.setFixedSize(200, 50)
        self.confirm_button.move(150, 195)

        self.confirm_button.clicked.connect(self.confirm_func)

    def confirm_func(self):
        
        self.w = None

        self.database = Main().database()

        if self.username.text() and self.password.text():
            
            if self.database.count_documents({"username_lower": self.username.text().lower()}) == 1:
                
                self.status = QtWidgets.QMessageBox(self)
                self.status.setWindowTitle("Successfully logged in!")
                self.status.setText("You have successfully logged in!")
                self.status.exec()
                self.hide()
                self.show_new_window()
            else:
                self.status = QtWidgets.QMessageBox(self)
                self.status.setWindowTitle("Error!")
                self.status.setText("Username or password is incorrect!")
                self.status.exec()
    
    def show_new_window(self):

        if self.w is None:
            self.w = loggedIn(self.username.text().lower())
        
        self.w.show()


class Main(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setFixedSize(500, 300)
        self.move(1000, 500)
        self.setWindowTitle("Secure Login System | FlatEarthGary")

        self.l_window = None
        self.r_window = None

        self.login_button = QPushButton(self)
        self.login_button.setFixedSize(500, 30)
        self.login_button.move(0, 70)
        self.login_button.setText("Login")

        self.register_button = QPushButton(self)
        self.register_button.setFixedSize(500, 30)
        self.register_button.move(0, 140)
        self.register_button.setText("Create account")

        self.login_button.clicked.connect(self.show_login_window)
        self.register_button.clicked.connect(self.show_reg_window)

    def show_login_window(self, checked):
        if self.l_window is None:
            self.l_window = login()
        self.l_window.show()
    
    def show_reg_window(self):
        if self.r_window is None:
            self.r_window = registration()
        self.r_window.show()

    def database(self):

        self.client = pymongo.MongoClient()
        self.db = self.client.LoginSystem
        self.users = self.db.users

        return self.users

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    app.exec_()
