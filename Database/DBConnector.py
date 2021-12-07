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
            self.cursor.execute(query, (user.name, user.mail, user.phone, user.imagepath, user.rankID))
            print(f'query de insert executada!!! rows inseridas: {self.cursor.rowcount}')
            self.connection.commit()
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
                ('Usuário',
                 'Fungicidas mais utilizados: Mancozebe, compostos à base de cobre, Enxofre, Piraclostrobina, '
                 'Azoxistrobina, Protioconazol, Fluxapiroxade'),

                ('Diretor de Divisão',
                 'Estado que mais utiliza agrotóxicos: Mato Grosso desponta como o campeão na compra de herbicidas, especialmente, o glifosato, líder brasileiro de vendas. '
                 'No estado, no Rio Grande do Sul e no Paraná, o consumo do glifosato é de 9 quilos a 19 quilos por hectare (ha).'),

                ('Ministro do Meio Ambiente',
                 'Registros de morte por agrotóxico: No Brasil, entre 2007 e 2014, foram registradas quase 2 mil mortes por intoxicação agrícola, '
                 'média de 148 óbitos por ano ou um caso a cada dois dias e meio. O campeão é o Paraná, com 231 falecimentos no período, '
                 'seguido por Pernambuco (151) e o trio São Paulo, Minas Gerais e Ceará (83 cada um).')
            ]
            query = Queries.QUERY_INSERT_RANKS
            self.cursor.executemany(query, ranks)
            self.connection.commit()
        except Error as E:
            print(f'[DEBUG] erro em create_ranks(): {E}')

    def get_users(self):
        self.cursor.execute(f'''SELECT * FROM USERS''')
        result = self.cursor.fetchall()
        return result

    def get_user_by_id(self, ID):
        self.cursor.execute(f'''SELECT * FROM USERS WHERE userID = "{ID}"''')
        result = self.cursor.fetchone()  # Retorna um único resultado da query
        if result:
            return result
        else:
            print('Usuário não encontrado')

    def get_user_by_name(self, name):
        self.cursor.execute(f'''SELECT * FROM USERS WHERE NAME = "{name}"''')
        result = self.cursor.fetchone()  # Retorna um único resultado da query
        if result:
            return result
        else:
            print('Usuário não encontrado')

    def show_user_by_id(self, ID):
        self.cursor.execute(f'''SELECT image FROM USERS WHERE userID = "{ID}"''')
        result = self.cursor.fetchone()  # Retorna um único resultado da query
        if result:
            self.__show_image(result)
        else:
            print('sem usuários cadastrados :)')
        return

    def __show_image(self, imagebytes):
        image = decode_image_from_uint8(imagebytes)

        # --- Display image
        cv2.imshow('Usuário logado', image)
        k = cv2.waitKey(0)
        if k == 27:  # wait for ESC key to exit
            cv2.destroyAllWindows()

    def get_rank_by_rankID(self, rankID):
        self.cursor.execute(f'''SELECT * FROM RANKS WHERE rankID = "{rankID}"''')
        result = self.cursor.fetchone()  # Retorna um único resultado da query
        if result:
            return result
        else:
            print('Rank não encontrado')

    def get_info_by_rankID(self, rankID):
        self.cursor.execute(f'''SELECT * FROM RANKS WHERE rankID < "{rankID + 1}"''')
        result = self.cursor.fetchall()  # Retorna um único resultado da query
        if result:
            return result
        else:
            print('Rank não encontrado')
