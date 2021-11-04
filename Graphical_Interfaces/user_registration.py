from sqlite3 import IntegrityError, Error
from tkinter import *
from tkinter import ttk, messagebox  # ttk serve para estilizar o tkinter - messagebox abre um pop-up
from tkinter import filedialog  # para abrir arquivos locais (nesse caso, uma imagem)

from PIL import ImageTk  # mostrar arquivo de imagem

import os  # Manusear arquivos e pastas
from os.path import dirname  # Controle de arquivos locais
from inspect import getsourcefile

import re  # para expressão regular

from Database.DBConnector import Database
from Utils.general import capitalize, User, DATABASE_FILE_PATH, translate_attributes
from Utils.ImageHandler import resize_image, encode_image_to_uint8

db = Database(DATABASE_FILE_PATH)


class EntryWithPlaceholder(Entry):
    """Classe que permite colocar placeholder em um "tkinter.Entry"""

    def __init__(self, master, text, color='grey'):
        super().__init__(master)

        # Define o texto e pegar o valor atual da cor da letra
        self.placeholder = text
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        # Binda o sistema de "perda" e "ganho" de foco (quando seleciona o elemento)
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        # Chama o método que coloca o placeholder
        self.put_placeholder()

    def put_placeholder(self):
        # Coloca o texto e cor no placeholder
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    # Elemento ganha foco -> remove o placeholder
    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    # Elemento perde foco -> adiociona o placeholder
    def foc_out(self, *args):
        if not self.get():  # Verifica se o usuário digitou algo
            self.put_placeholder()


class RegisterRoot(Tk):
    def __init__(self):
        super(RegisterRoot, self).__init__()
        self.title("Cadastro de usuário")  # Define o título da janela
        self.geometry("600x600")  # Dimensões da janela
        self.resizable(False, False)  # Desliga a função de redimensionar a janela (X, Y)

        # Divide a janela em 2 colunas (esquerda / direita)
        # Esquerda:
        self.labelLeft = ttk.LabelFrame(self)
        self.labelLeft.pack(side=LEFT, fill=BOTH, expand=1)

        # Direita:
        self.labelRight = ttk.LabelFrame(self)
        self.labelRight.pack(side=RIGHT, fill=BOTH, expand=1)

        # ------------------- Labels: elementos que apareceram na interface ------------------- #

        # Nome do usuário:
        self.labelFrameUsername = ttk.LabelFrame(self.labelLeft, text="Nome do usuário*")  # Define a label
        self.labelFrameUsername.pack(side=TOP, expand=1, padx=20, pady=20, anchor=W)  # Posiciona a label na janela
        self._username_button()  # Chama o método que permitirá o input do NOME

        # Input imagem do usuário:
        self.labelFrameImage = ttk.LabelFrame(self.labelLeft, text="Foto de cadastro*")
        self.labelFrameImage.pack(side=TOP, expand=1, padx=20, pady=20, anchor=W)
        self._image_name_label()
        self._image_button()

        # Display imagem do usuário:
        self.labelFrameImageDisplay = ttk.LabelFrame(self.labelLeft, text="Visualização da foto:")
        self.labelFrameImageDisplay.pack(side=TOP, expand=1, padx=20, pady=20, anchor=W)
        self._image_display()

        # Email do usuário:
        self.labelFrameEmail = ttk.LabelFrame(self.labelRight, text="Email*")
        self.labelFrameEmail.pack(side=TOP, expand=1, padx=20, pady=20, anchor=W)
        self._email_button()

        # Telefone do usuário:
        self.labelFramePhone = ttk.LabelFrame(self.labelRight, text="Número de telefone*\n(com DDD)")
        self.labelFramePhone.pack(side=TOP, expand=1, padx=20, pady=20, anchor=W)
        self._phone_button()

        # Nível rank do usuário:
        self.labelFrameLevel = ttk.LabelFrame(self.labelRight, text="Nível de acesso*")
        self.labelFrameLevel.pack(side=TOP, expand=1, padx=20, pady=20, anchor=W)
        self.rankLevel = IntVar()
        self._level_button()

        # Botão de enviar:
        self.labelFrameSubmitButton = ttk.Label(self.labelRight)
        self.labelFrameSubmitButton.pack(side=BOTTOM, expand=1, padx=20, pady=20, anchor=W)
        self._submit_button()

        # User input data:
        self.username = ''
        self.user_image_file = ''
        self.user_image_encoded = ''
        self.email = ''
        self.phone = ''
        self.rank = 0

    # ------------------- Handlers : configuram e adicionam os elementos na interface ------------------- #

    def _username_button(self):
        self.username_button = EntryWithPlaceholder(self.labelFrameUsername, text='Nome Completo')
        self.username_button.pack(anchor=W)

    def _image_button(self):
        self.image_button = ttk.Button(self.labelFrameImage, text="Selecione a imagem", command=self.browse_files)
        self.image_button.pack(anchor=W)

    def _image_name_label(self):
        self.imagelabel = ttk.Label(self.labelFrameImage, text='')

    def _image_display(self):
        os.chdir((dirname(getsourcefile(lambda: 0))))
        resizedimg = resize_image(r'../Images/default_user_image.png')
        if resizedimg:
            render = ImageTk.PhotoImage(resizedimg)
            self.image_display = Label(self.labelFrameImageDisplay, image=render)
            self.image_display.image = render
            self.image_display.pack(anchor=W)

    def _email_button(self):
        self.email_button = EntryWithPlaceholder(self.labelFrameEmail, text='email@domínio.com')
        self.email_button.pack(anchor=W)

    def _phone_button(self):
        self.phone_button = EntryWithPlaceholder(self.labelFramePhone, text='[apenas números]')
        self.phone_button.pack(anchor=W)

    def _level_button(self):
        self.level_button_1 = ttk.Radiobutton(self.labelFrameLevel,
                                              text="Usuário                   [acesso nível básico]",
                                              variable=self.rankLevel,
                                              value=1)
        self.level_button_1.pack(anchor=W)

        self.level_button_2 = ttk.Radiobutton(self.labelFrameLevel, text="Diretor de divisão  [acesso nível avançado]",
                                              variable=self.rankLevel,
                                              value=2)
        self.level_button_2.pack(anchor=W)

        self.level_button_3 = ttk.Radiobutton(self.labelFrameLevel,
                                              text="Ministro                  [admin/acesso total]",
                                              variable=self.rankLevel,
                                              value=3)
        self.level_button_3.pack(anchor=W)

    def _submit_button(self):
        self.submit_button = ttk.Button(self.labelFrameSubmitButton, text="Cadastrar usuário", command=self.submit)
        self.submit_button.pack(anchor=W)

    # -------------------------------------- Métodos e funções -------------------------------------- #

    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo de imagem",
                                              filetype=(("jpeg", "*.jpg"), ("png", "*.png")))
        self.imagelabel.config(text='')
        self.imagelabel.text = ''
        self.imagelabel.configure(text=filename if len(filename) < 35 else '%.35s' % filename + '...')
        self.imagelabel.pack()
        self.user_image_file = filename
        print(self.user_image_file)

        # Atualiza a imagem do usuário no front
        resizedimg = resize_image(self.user_image_file)  # Chama a função para redimencionar a imagem
        if resizedimg:
            render = ImageTk.PhotoImage(resizedimg)  # Renderiza a imagem (para ser compativel com a Label)
            self.image_display.configure(image=render)  # Configura a imagem
            self.image_display.image = render  # Limpa o "cache" da propriedade "imagem"

    def verify_inputs(self):
        if not re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', self.username):
            messagebox.showinfo("Entrada inválida [Nome do usuário]", "Preencha o nome do usuário corretamente.")

        elif not os.path.isfile(self.user_image_file):
            messagebox.showinfo("Erro em imagem", "Favor, selecione uma imagem para cadastrar o usuário.")

        elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.email):
            messagebox.showinfo("Entrada inválida [email]", "Preencha o email do usuário corretamente.")

        elif not re.fullmatch(r'^(?:[12][1-9]9[2-9]|[3-9][1-9][5-9])[0-9]{7}$', self.phone):
            messagebox.showinfo("Entrada inválida [telefone]",
                                "Preencha o telefone do usuário corretamente.\n[Passar o DDD é obrigatório]")

        elif self.rank not in (1, 2, 3):
            messagebox.showinfo("Entrada inválida [nível de acesso]",
                                "Preencha o nível de rank corretamente")
        else:
            return True

    def update_inputs(self):
        self.username = capitalize(self.username_button.get())
        self.user_image_encoded = encode_image_to_uint8(self.user_image_file)
        self.email = str(self.email_button.get()).lower()
        self.phone = re.sub(r'[ \t]+', '', re.sub('/[^0-9]/', '', self.phone_button.get()))
        self.rank = self.rankLevel.get()

    def submit(self):
        self.update_inputs()
        valid_input = self.verify_inputs()

        if valid_input:
            user = User(name=self.username, mail=self.email, phone=self.phone, image=self.user_image_encoded,
                        rankID=self.rank)

            try:
                user_inserted = db.create_user(user)

                if isinstance(user_inserted, IntegrityError):
                    messagebox.showerror("Chave única repetida",
                                         "Um dos campos preenchidos já está cadastrado no banco:\n"
                                         f"{translate_attributes(str(user_inserted).split('Users.')[1])}")
                elif isinstance(user_inserted, Error):
                    messagebox.showerror("Erro inesperado aconteceu",
                                         "Um erro fatal aconteceu:\n"
                                         f"{user_inserted}")
                else:
                    messagebox.showinfo("Usuário criado",
                                        "O usuário foi criado com sucesso:\n"
                                        f"{user.get_values()}")
                    self.destroy()

            except Exception as E:
                print(f'[DEBUG] erro em create_user() dentro de submit(): {E}')
