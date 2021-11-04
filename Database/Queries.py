# Definindo queries constantes para não poluir o código com queries longas

QUERY_CREATE_TABLE_RANKS = """
            CREATE TABLE IF NOT EXISTS Ranks (
                rankID INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL
            );"""

QUERY_CREATE_TABLE_USERS = """
            CREATE TABLE IF NOT EXISTS Users (
                userID INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                mail TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL UNIQUE,
                image blob NOT NULL,
                rankID INTEGER DEFAULT 1,
                FOREIGN KEY(rankID) REFERENCES Ranks(rankID)
            );
        """

QUERY_INSERT_USER = """INSERT INTO USERS(name,mail,phone,image,rankID) VALUES (?,?,?,?,?)"""

QUERY_INSERT_RANKS = """INSERT INTO RANKS(name,description) VALUES (?,?)"""
