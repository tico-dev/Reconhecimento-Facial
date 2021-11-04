import os
from config import ROOT_DIR

DATABASE_FILENAME = "database.db"
DATABASE_FILE_PATH = os.path.join(ROOT_DIR, 'Database', DATABASE_FILENAME)
IMAGES_PATH = os.path.join(ROOT_DIR, 'Images')


def capitalize(text):
    return ' '.join([x.capitalize() for x in text.split(' ')])


def translate_attributes(attributes):
    return str(attributes).lower().replace('name', 'Nome').replace('mail', 'Email').replace('phone', 'Telefone')


class User:
    def __init__(self, name, mail, phone, image, rankID):
        self.name = name
        self.mail = mail
        self.phone = phone
        self.image = image
        self.rankID = rankID

    def get_values(self):
        return (f'Nome: {self.name}\n'
                f'Mail: {self.mail}\n'
                f'Phone: {self.phone}\n'
                f'RankID: {self.rankID}')

    def get_attributes(self):
        return ['name', 'mail', 'phone', 'image', 'rankID']
