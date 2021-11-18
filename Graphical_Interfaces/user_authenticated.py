import io
from tkinter import *
from tkinter import ttk  # ttk serve para estilizar o tkinter - messagebox abre um pop-up

import PIL.Image

from PIL import ImageTk  # mostrar arquivo de imagem

from Database.DBConnector import Database
from Utils.general import capitalize, User, DATABASE_FILE_PATH, translate_attributes

db = Database(DATABASE_FILE_PATH)   # instância o banco de dados


class AuthenticatedRoot(Tk):
    def __init__(self, user: User):
        super(AuthenticatedRoot, self).__init__()

        self.user = user

        self.title(f"Usuário autenticado: {self.user.name}")  # Define o título da janela
        self.geometry("600x600")  # Dimensões da janela
        self.resizable(False, False)  # Desliga a função de redimensionar a janela (X, Y)

        self.finished = False
        self.rank_info = []

        # Divide a janela em 2 colunas (esquerda / direita)
        # Esquerda:
        self.labelLeft = ttk.LabelFrame(self)
        self.labelLeft.pack(side=LEFT, fill=BOTH, expand=1)

        # Direita:
        self.labelRight = ttk.LabelFrame(self)
        self.labelRight.pack(side=RIGHT, fill=BOTH, expand=1)

        # ------------------- Labels: elementos que apareceram na interface ------------------- #

        # Nome do usuário:
        self.labelFrameUsername = ttk.LabelFrame(self.labelLeft, text="Nome do usuário:")  # Define a label
        self.labelFrameUsername.pack(side=TOP, expand=1, padx=20, anchor=W, fill=X)  # Posiciona a label na janela
        self._username_textlabel()  # Chama o método que permitirá o mostrar o NOME

        # Rank do usuário:
        self.labelFrameRank = ttk.LabelFrame(self.labelLeft, text="Level de acesso:")  # Define a label
        self.labelFrameRank.pack(side=TOP, expand=1, padx=20, anchor=W, fill=X)  # Posiciona a label na janela
        self._level_textlabel()  # Chama o método que permitirá o mostrar o RANK

        # Email do usuário:
        self.labelFrameEmail = ttk.LabelFrame(self.labelLeft, text="Email:")
        self.labelFrameEmail.pack(side=TOP, expand=1, padx=20, anchor=W, fill=X)
        self._email_textlabel()

        # Telefone do usuário:
        self.labelFramePhone = ttk.LabelFrame(self.labelLeft, text="Telefone:")
        self.labelFramePhone.pack(side=TOP, expand=1, padx=20, anchor=W, fill=X)
        self._phone_textlabel()

        # Display imagem do usuário:
        self.labelFrameImageDisplay = ttk.LabelFrame(self.labelLeft, text="Imagem do usuário:")
        self.labelFrameImageDisplay.pack(side=TOP, expand=1, padx=20, pady=20, anchor=W, fill=X)
        self._image_display()

        self.labelFrameInformations = ttk.LabelFrame(self.labelRight, text='Informações disponíveis para seu rank:')
        self.labelFrameInformations.pack(side=TOP, expand=1, fill=BOTH)
        self._informations_textlabel()

        # Botão de enviar:
        self.labelFrameSubmitButton = ttk.Label(self.labelRight)
        self.labelFrameSubmitButton.pack(side=BOTTOM, pady=10, anchor=W, fill=X)
        self._logout_button()

    # ------------------- Handlers : configuram e adicionam os elementos na interface ------------------- #

    def _username_textlabel(self):
        self.username_textlabel = ttk.Label(self.labelFrameUsername, text=self.user.name)
        self.username_textlabel.pack(anchor=W, fill=X)

    def _level_textlabel(self):
        for result in db.get_info_by_rankID(self.user.rankID):
            self.rank_info.append(result[2])

        _user_rankdata = db.get_rank_by_rankID(self.user.rankID)

        _rankid = _user_rankdata[0]
        _rankname = _user_rankdata[1]
        _rankdescription = _user_rankdata[2]
        self.level_textlabel = ttk.Label(self.labelFrameRank, text=f'[{_rankid}] {_rankname}')
        self.level_textlabel.pack(anchor=W, fill=X)

    def _image_display(self):
        img = PIL.Image.open(io.BytesIO(self.user.imagepath))

        width_percent = (200 / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        resizedimg = img.resize((200, height_size), PIL.Image.ANTIALIAS)

        b = io.BytesIO()

        resizedimg.save(b, format="jpeg")
        if resizedimg:
            render = ImageTk.PhotoImage(resizedimg)
            self.image_display = Label(self.labelFrameImageDisplay, image=render)
            self.image_display.image = render
            self.image_display.pack(anchor=W, fill=BOTH)

    def _informations_textlabel(self):
        print(f'array : {self.rank_info}')
        self.information_textlabel = ttk.Label(self.labelFrameInformations, text='\n\n\n'.join([x for x in self.rank_info]), wraplength=300)
        self.information_textlabel.pack(side=TOP, anchor=N, fill=BOTH, expand=1)

    def _email_textlabel(self):
        self.email_textlabel = ttk.Label(self.labelFrameEmail, text=self.user.mail)
        self.email_textlabel.pack(anchor=W, fill=X)

    def _phone_textlabel(self):
        self.phone_textlabel = ttk.Label(self.labelFramePhone, text=self.user.phone)
        self.phone_textlabel.pack(anchor=W, fill=X)

    def _logout_button(self):
        self.logout_button = ttk.Button(self.labelFrameSubmitButton, text="Finalizar sessão", command=self.logout)
        self.logout_button.pack(anchor=W, fill=X)

    def logout(self):
        self.finished = True
