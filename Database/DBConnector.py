import sqlite3
from sqlite3 import Error, IntegrityError

import cv2

import Database.Queries as Queries
from Utils.ImageHandler import decode_image_from_uint8
from Utils.general import User


class Database:
    def __init__(self, db_file_path):
        """Método construtor da classe"""
        # Atributos que guardam o Objeto de conexão/cursor
        self.connection = None
        self.cursor = None

        try:
            self.__create_connection(db_file_path)
        except Error as E:
            print(f'[DEBUG] erro no método construtor: {E}')

    def __create_connection(self, db_file_path):
        """Cria uma conexão com um banco de dados SQLite"""
        try:
            dbfile = db_file_path
            self.connection = sqlite3.connect(dbfile)
            self.cursor = self.connection.cursor()

            self.__setup_tables()  # Cria as tabelas (se não existirem)

            # Se conexão foi feita:
            print(f"Conexão criada com sucesso.\nVersão SQLite: {sqlite3.version}")
            return self.connection

        except Error as E:
            # Se execução deu erro:
            print(f'[DEBUG]: erro na função __create_connection: {E}')
            return False

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexão finalizada.")

    def __user_exists(self, username):
        try:
            self.cursor.execute(f"SELECT * FROM USERS WHERE name = '{username}'")
            result = self.cursor.fetchall()
            if len(result) > 0:
                return True
            return False
        except Error as E:
            print(f'[DEBUG] erro em __user_exists(): {E}')

    def __ranks_exists(self):
        try:
            self.cursor.execute(f"SELECT * FROM RANKS")
            result = self.cursor.fetchall()
            print(self.cursor.fetchall())
            print(result)
            if len(result) > 0:
                return True
            return False
        except Error as E:
            print(f'[DEBUG] erro em __ranks_exists(): {E}')

    # -------------------------------------------------------------------------------
    # SETUP DAS TABELAS:
    def __setup_tables(self):
        try:
            self.__create_table_ranks()
            self.__create_table_users()
        except Error as E:
            print(f'[DEBUG] erro em __setup_tables(): {E}')

    def __create_table_ranks(self):
        query = Queries.QUERY_CREATE_TABLE_RANKS
        try:
            self.cursor.execute(query)
            if not self.__ranks_exists():
                self.__create_ranks()  # Insere os ranks na tabela

        except Error as E:
            print(f'[DEBUG] erro em __create_table_ranks(): {E}')

    def __create_table_users(self):
        query = Queries.QUERY_CREATE_TABLE_USERS
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Error as E:
            print(f'[DEBUG] erro em __create_table_users(): {E}')

    # -------------------------------------------------------------------------------
    # POPULANDO AS TABELAS:
    def create_user(self, user: User):
        user_created = None
        try:
            query = Queries.QUERY_INSERT_USER
            self.cursor.execute(query, (user.name, user.mail, user.phone, user.image, user.rankID))
            print(f'query de insert executada!!! rows inseridas: {self.cursor.rowcount}')
            self.connection.commit()
            self.__show_user(user.name)
            user_created = True

        except IntegrityError as E:
            user_created = E

        except Error as E:
            print(f'[DEBUG] erro em create_user(): {E}')
            user_created = E

        finally:
            return user_created

    def __create_ranks(self):
        try:
            ranks = [
                ('Usuário', 'Cargo padrão'),

                ('Direto de Divisão',
                 'Cargo exclusivo para os diretores de divisões. Acesso à informações confidenciais'),

                ('Ministro do Meio Ambiente',
                 'Cargo exclusivo para o responsável pelo Ministério do Meio Ambiente. Acesso à todas informações')
            ]
            query = Queries.QUERY_INSERT_RANKS
            self.cursor.executemany(query, ranks)
            self.connection.commit()
        except Error as E:
            print(f'[DEBUG] erro em create_ranks(): {E}')

    def __show_user(self, name):
        print("show user foi chado!!!")
        self.cursor.execute(f'''SELECT image FROM USERS WHERE NAME = "{name}"''')
        result = self.cursor.fetchone()[0]  # Retorna um único resultado da query
        print('passou do result')
        self.__show_image(result)
        print('teoricamente chamou o show image')
        return

    def __show_image(self, imagebytes):
        print("show image foi chado!!!")
        image = decode_image_from_uint8(imagebytes)

        # --- Display image
        cv2.imshow('image', image)
        k = cv2.waitKey(0)
        if k == 27:  # wait for ESC key to exit
            cv2.destroyAllWindows()

#
# if __name__ == '__main__':
#     db = Database()
#     connection = db.create_connection(DATABASE_FILE_PATH)  # Concatena o caminho atual + nome do arquivo .db
#     db.create_user()
#     db.close_connection()  # Finaliza a conexão com o banco de dados.
