#Importa as classes das bibliotecas
from PySide6.QtWidgets import (
    QApplication, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QFrame, QCheckBox, QDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QColor
from Backend import AccountBackend
import sys
import re

#O TopBar é onde fica a foto azul de plano de fundo na parte superior do painel.
class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        #Tamanho fixo.
        self.setFixedSize(350, 140)

        #plano de fundo.
        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap("images/TopBar.png"))
        self.bg.setScaledContents(True)
        self.bg.setGeometry(0, 0, self.width(), self.height())
        self.bg.lower()

#A classe de login é onde ficam os campos de login e botões.
class Login(QFrame):
    def __init__(self):
        super().__init__()

        #Importa a classe de contas do arquivo Backend.py
        self.account = AccountBackend()

        #Texto que avisa onde preencher o username.
        self.user_label = QLabel("👤 User")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setFixedWidth(90)

        #Caixa de texto para preencher username.
        self.user_lineedit = QLineEdit()
        self.user_lineedit.setPlaceholderText("Insert your username")
        self.user_lineedit.setStyleSheet('''
                QLabel {
                color: #5a5a5a;}
                QLineEdit {
                background-color: #e6e9ee;
                color: #1e1e1e;
                border: 1px solid #b0b6bf;
                border-radius: 6px;
                padding: 8px;}
                QLineEdit:focus {
                border: 1px solid #3a86ff;
                background-color: #edf0f5;}''')

        #Alinha o texto "User" com a caixa de texto horizontalmente.
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_lineedit)

        #Texto que avisa onde preencher a senha.
        self.password_label = QLabel("🔐 Password")
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_label.setFixedWidth(90)

        #Caixa de texto para preencher a senha.
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setPlaceholderText("Insert your password")
        self.password_lineedit.setStyleSheet('''
                QLabel {
                color: #5a5a5a;}
                QLineEdit {
                background-color: #e6e9ee;
                color: #1e1e1e;
                border: 1px solid #b0b6bf;
                border-radius: 6px;
                padding: 8px;}
                QLineEdit:focus {
                border: 1px solid #3a86ff;
                background-color: #edf0f5;}''')

        #Alinha o texto "Password" com a caixa de texto horizontalmente.
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_lineedit)

        #Faz o check box para manter as informações previamente inseridas.
        self.rememberme_box = QCheckBox()
        self.rememberme_box.setText("Remember me")

        #Botão de login
        self.login_btn = QPushButton()
        self.login_btn.setText("Login")
        self.login_btn.setStyleSheet('''
                QPushButton {
                background-color: #3a86ff;
                color: white;
                border-radius: 8px;
                height: 36px;
                font-size: 14px;}
                QPushButton:hover {
                background-color: #5a9bff;}''')

        #Chama o metodo pressed_login
        self.login_btn.clicked.connect(self.pressed_login)

        #efeito de sombreamento no botão de login.
        shadow = QGraphicsDropShadowEffect(self.login_btn)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.login_btn.setGraphicsEffect(shadow)

        #layout que alinha o botão remember me e botão de login na vertical.
        login_layout = QVBoxLayout()
        login_layout.addWidget(self.rememberme_box)
        login_layout.addWidget(self.login_btn)

        #texto que mostra se o login foi bem sucedido ou não
        self.warning_text = QLabel()

        #signup button
        self.signup_btn = QPushButton()
        self.signup_btn.setText("Sign up")
        self.signup_btn.setFlat(True)
        self.signup_btn.setCursor(Qt.PointingHandCursor)
        self.signup_btn.setStyleSheet('''
                QPushButton {
                background-color: #c8c8c8;
                color: blue;
                border-radius: 8px;
                height: 36px;
                font-size: 14px;}
                QPushButton:hover {
                background-color: #cfcfcf;}''')
        self.signup_btn.clicked.connect(self.signup_screen)

        #Efeito de sombreamento no botão de sign up
        shadow = QGraphicsDropShadowEffect(self.signup_btn)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.signup_btn.setGraphicsEffect(shadow)

        #this is the final layout
        horizontal_layout = QVBoxLayout()
        horizontal_layout.setContentsMargins(60, 5, 60, 5)
        horizontal_layout.setSpacing(5)
        horizontal_layout.addStretch()
        horizontal_layout.addLayout(user_layout)
        horizontal_layout.addLayout(password_layout)
        horizontal_layout.addLayout(login_layout)
        horizontal_layout.addWidget(self.warning_text)
        horizontal_layout.addWidget(self.signup_btn)
        horizontal_layout.addStretch()
        self.setLayout(horizontal_layout)

    #Esse metodo transfere os dados inseridos para o arquivo Backend para procurar pela tabela referente ao usuário
    def pressed_login(self):
        if not all ([self.user_lineedit.text(), self.password_lineedit.text()]):
            self.warning_text.setText('Fill all fields above')
            self.warning_text.setStyleSheet('color: red')
            return
        success = self.account.login_account(
            username=self.user_lineedit.text(),
            password=self.password_lineedit.text()
        )
        if success:
            self.warning_text.setText('Login successful')
            self.warning_text.setStyleSheet('color: green')
        else:
            self.warning_text.setText('Login failed')
            self.warning_text.setStyleSheet('color: red')

    #Esse metodo abre a tela de signup quando o usuário clica no botão certo.
    def signup_screen(self):
        dialog = Signup()
        dialog.exec_()

#Essa classe é a tela que é aberta sempre que o usuário clica em signup
class Signup(QDialog):
    def __init__(self):
        super().__init__()

        #importa a classe AccountBackend do arquivo Backend
        self.account = AccountBackend()

        #configurações geral da tela
        self.setWindowTitle('Signup')
        self.setFixedSize(360, 400)
        self.setWindowIcon(QIcon('images/workspace_icon.png'))
        self.setStyleSheet('background-color: #bbbbbb;')

        #definições do card
        self.card = QFrame()
        self.card.setAttribute(Qt.WA_StyledBackground, True)
        self.card.setStyleSheet('''
                background-color: white;
                border-radius: 14px;''')

        #efeito de sombreamento do card
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.card.setGraphicsEffect(shadow)


        #Título
        self.title_label = QLabel('Create your Account')
        self.title_label.setStyleSheet('''
        QLabel {
        color: #5170ff;
        font-family: 'Open Sans';
         font-size: 20px;
         font-weight: bold;}''')

        #Subtítulo
        self.subtitle_label = QLabel('Sign up to get started!')
        self.subtitle_label.setStyleSheet('''
        QLabel {
        color: #737373;
        font-size: 14px;}''')

        #caixa de texto para Primeiro nome
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText('First Name')
        self.first_name.setStyleSheet('''
                QLabel {
                color: #5a5a5a;}
                QLineEdit {
                background-color: #e6e9ee;
                color: #1e1e1e;
                border: 1px solid #b0b6bf;
                border-radius: 6px;
                padding: 8px;}
                QLineEdit:focus {
                border: 1px solid #3a86ff;
                background-color: #edf0f5;}''')

        #Caixa de texto para Ultimo nome
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText('Last Name')
        self.last_name.setStyleSheet('''
                QLabel {
                color: #5a5a5a;}
                QLineEdit {
                background-color: #e6e9ee;
                color: #1e1e1e;
                border: 1px solid #b0b6bf;
                border-radius: 6px;
                padding: 8px;}
                QLineEdit:focus {
                border: 1px solid #3a86ff;
                background-color: #edf0f5;}''')

        #Caixa de texto para nome de usuário
        self.username = QLineEdit()
        self.username.setPlaceholderText('Username')
        self.username.setStyleSheet('''
                QLabel {
                color: #5a5a5a;}
                QLineEdit {
                background-color: #e6e9ee;
                color: #1e1e1e;
                border: 1px solid #b0b6bf;
                border-radius: 6px;
                padding: 8px;}
                QLineEdit:focus {
                border: 1px solid #3a86ff;
                background-color: #edf0f5;}''')

        #Caixa de texto para senha
        self.password = QLineEdit()
        self.password.setPlaceholderText('Password')
        self.password.setStyleSheet('''
                QLabel {
                color: #5a5a5a;}
                QLineEdit {
                background-color: #e6e9ee;
                color: #1e1e1e;
                border: 1px solid #b0b6bf;
                border-radius: 6px;
                padding: 8px;}
                QLineEdit:focus {
                border: 1px solid #3a86ff;
                background-color: #edf0f5;}''')

        #Botão de Singnup
        self.signup_btn = QPushButton()
        self.signup_btn.setText("Sign Up")
        self.signup_btn.setStyleSheet('''
                QPushButton {
                background-color: #3a86ff;
                color: white;
                border-radius: 8px;
                height: 36px;
                font-size: 14px;}
                QPushButton:hover {
                background-color: #5a9bff;}''')
        self.signup_btn.clicked.connect(self.pressed_signup)

        #Texto de aviso.
        self.warning_text = QLabel(' ')


        #layout para primeiro e segundo nome
        full_name_layout = QHBoxLayout()
        full_name_layout.addWidget(self.first_name)
        full_name_layout.addWidget(self.last_name)

        #layout vertical do card
        vertical_layout = QVBoxLayout(self.card)
        vertical_layout.setContentsMargins(30, 0, 30, 0)
        vertical_layout.addStretch()
        vertical_layout.addWidget(self.title_label)
        vertical_layout.addWidget(self.subtitle_label)
        vertical_layout.addSpacing(30)
        vertical_layout.addLayout(full_name_layout)
        vertical_layout.addWidget(self.username)
        vertical_layout.addWidget(self.password)
        vertical_layout.addWidget(self.signup_btn)
        vertical_layout.addWidget(self.warning_text)
        vertical_layout.addStretch()

        #Layout final.
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(self.card)

        self.setLayout(main_layout)

    #Esse metodo transfere todos os dados para o metodo create_account do arquivo Backend, onde o novo usuário é salvo.
    def pressed_signup(self):
        if not all([
            self.first_name.text(),
            self.last_name.text(),
            self.username.text(),
            self.password.text()
        ]):
            self.warning_text.setStyleSheet('color:red')
            self.warning_text.setText('Fill all fields above')
            return

        password = self.password.text()

        valid, message = self.validate_password(password)
        if not valid:
            self.warning_text.setStyleSheet('color:red')
            self.warning_text.setText(message)
            return

        success = self.account.create_account(
        username=self.username.text(),
        first_name=self.first_name.text(),
        last_name=self.last_name.text(),
        password=self.password.text(),)

        if success:
            self.warning_text.setStyleSheet('color:green')
            self.warning_text.setText('Sign up successful')
        else:
            self.warning_text.setStyleSheet('color:red')
            self.warning_text.setText('Sign up failed')

    #Esse metodo serve para que o usuário não consiga fazer qualquer tipo de senha
    def validate_password(self, password: str):
        if len(password) < 8:
            return False, "Password must be at least 8 characters."

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."

        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."

        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number."

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character."

        return True, ""

#A classe MainWindow é responsável por organizar a posição do TopBar e Login e iniciar software
class MainWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(350, 400)
        self.setWindowIcon(QIcon("images/workspace_icon.png"))

        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.TopBar = TopBar()
        self.Login = Login()

        root.addWidget(self.TopBar)
        root.addWidget(self.Login)

        self.setLayout(root)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())