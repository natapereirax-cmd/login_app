#Importa as classes e as bibliotecas.
import sqlite3, hashlib, os
DB_NAME = 'database.db'

#Essa é a classe que guarda todos os metodos referentes à criação e administração dos dados
class AccountBackend:
    def __init__(self):

        #definimos as funções de conexão com o arquivo .db e funções SQL
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        #Chama o metodo de criação de tabela
        self.create_table()

    #função para criar a tabela de usuarios
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL)''')
        self.conn.commit()

    #Metodo para a criptografia de senhas.
    def hash_password(self, password: str, salt: bytes) -> str:
        return hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                100000,
            ).hex()

    #Esse metodo verifica se a senha salva entra em acordo com os dados impostos pelo usuário previalmente.
    def verify_password(self, password: str, stored_hash: str, salt: bytes) -> bool:
        return self.hash_password(password, salt) == stored_hash

    #Cria uma conta de acordo com os dados importados do usuário.
    def create_account(self, username, first_name, last_name, password):
        salt = os.urandom(16)
        password_hash = self.hash_password(password, salt)
        try:
            self.cursor.execute('''INSERT INTO accounts(username, first_name, last_name, password_hash, salt)
            VALUES(?, ?, ?, ?, ?)''', (username, first_name, last_name, password_hash, salt.hex()))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    #Esse metodo recebe os dados do usuário e confere se de fato eles existem no banco de dados.
    def login_account(self, username: str, password: str) -> int | None:
        self.cursor.execute(
            '''SELECT id, password_hash, salt
               FROM accounts
               WHERE username = ?''',
            (username,)
        )

        row = self.cursor.fetchone()

        if not row:
            return None

        internal_id, stored_hash, salt_hex = row
        salt = bytes.fromhex(salt_hex)

        if self.verify_password(password, stored_hash, salt):
            return internal_id

        return None