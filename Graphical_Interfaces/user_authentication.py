import os

import cv2

from Database.DBConnector import Database
from Graphical_Interfaces.identify_user import recognize_face
from Utils.ImageHandler import decode_image_from_uint8

from Utils.general import DATABASE_FILE_PATH, IMAGES_PATH, User


class Authenticator:
    def __init__(self):
        self.connection = Database(DATABASE_FILE_PATH)
        self.users = []
        self._populate_users()

    def _populate_users(self):
        users = self.connection.get_users()

        # row[4]: image
        for row in users:
            user_ID = str(row[0])
            user_name = row[1]
            user_mail = row[2]
            user_phone = row[3]
            user_imagebinary = row[4]
            user_rankID = row[5]

            user_imgpath = os.path.join(IMAGES_PATH, user_ID)
            user_imgname = str(user_name) + '.jpg'
            user_imgfullpath = os.path.join(user_imgpath, user_imgname)

            if not os.path.exists(user_imgpath):
                os.makedirs(user_imgpath)

            if not cv2.imwrite(user_imgfullpath, decode_image_from_uint8(user_imagebinary)):
                raise Exception('Não conseguiu salvar imagem')

            user = User(
                user_ID, user_name, user_mail, user_phone, user_imgfullpath, user_rankID
            )
            self.users.append(user)

    def identify_user(self):
        return recognize_face(self.users)


if __name__ == '__main__':
    root = Authenticator()
    print(root.identify_user())
