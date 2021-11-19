import os

from config import ROOT_DIR

DATABASE_FILENAME = "database.db"
DATABASE_FILE_PATH = os.path.join(ROOT_DIR, 'Database', DATABASE_FILENAME)
IMAGES_PATH = os.path.join(ROOT_DIR, 'Images')


def capitalize(text):
    return ' '.join([x.capitalize() for x in text.split(' ')])


def translate_attributes(attributes):
    return str(attributes).lower().replace('name', 'Nome').replace('mail', 'Email').replace('phone', 'Telefone')


def image_from_bin_to_file(img_binary):
    pass


class User:
    def __init__(self, ID=None, name=None, mail=None, phone=None, image=None, rankID=None):
        self.ID = ID
        self.name = name
        self.mail = mail
        self.phone = phone
        self.imagepath = image
        self.rankID = rankID

    def validate_user(self):
        if not self.ID or not self.name or not self.mail or not self.phone or not self.imagepath or not self.rankID:
            return False
        else:
            return True

    def show_values(self):
        if not self.ID:
            return f'Nome: {self.name}\n' \
                   f'Email: {self.mail}\n' \
                   f'Telefone: {self.phone}\n' \
                   f'IDCargo: {self.rankID}'
        else:
            return f'ID: {self.ID}\n' \
                   f'Nome: {self.name}\n' \
                   f'Email: {self.mail}\n' \
                   f'Telefone: {self.phone}\n' \
                   f'IDCargo: {self.rankID}'
