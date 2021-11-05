from tkinter import *
from tkinter import ttk, messagebox  # ttk serve para estilizar o tkinter - messagebox abre um pop-up
from tkinter import filedialog  # para abrir arquivos locais (nesse caso, uma imagem)

from PIL import ImageTk  # mostrar arquiv1o de imagem

import os  # Manusear arquivos e pastas
from os.path import dirname  # Controle de arquivos locais
from inspect import getsourcefile

from Utils.ImageHandler import resize_image, decode_image_from_uint8, encode_image_to_uint8


class AuthenticatorRoot(Tk):
    def __init__(self):
        super(AuthenticatorRoot, self).__init__()
        self.title("Identificação de usuário")  # Define o título da janela
        self.geometry("600x600")  # Dimensões da janela
        self.resizable(False, False)  # Desliga a função de redimensionar a janela (X, Y)

        # ------------------- Labels: elementos que apareceram na interface ------------------- #

        # Display imagem do usuário:
        self.labelFrameImageDisplay = ttk.LabelFrame(self, text="Visualização da foto:")
        self.labelFrameImageDisplay.pack(side=TOP, expand=1, pady=20)
        self._image_display()

        # Input imagem do usuário:
        self.labelFrameImage = ttk.LabelFrame(self, text="Foto de cadastro*")
        self.labelFrameImage.pack(side=TOP, expand=1, pady=20)
        self._image_name_label()
        self._image_button()

        # Botão de enviar:
        self.labelFrameSubmitButton = ttk.Label(self)
        self.labelFrameSubmitButton.pack(side=BOTTOM, expand=1, padx=20, pady=20, anchor=W)
        self._submit_button()

    # ------------------- Handlers : configuram e adicionam os elementos na interface ------------------- #

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


    def _submit_button(self):
        self.submit_button = ttk.Button(self.labelFrameSubmitButton, text="Cadastrar usuário", command=self.submit)
        self.submit_button.pack(anchor=W)

    # -------------------------------------- Métodos e funções -------------------------------------- #

    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo de imagem",
                                              filetype=(("jpeg", "*.jpg"), ("jpeg", "*.jpeg"), ("png", "*.png")))
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

    def verify_input(self):
        if not os.path.isfile(self.user_image_file):
            messagebox.showinfo("Erro em imagem", "Favor, selecione uma imagem para cadastrar o usuário.")

        else:
            return True

    def submit(self):
        valid_input = self.verify_input()

        if valid_input:
            # TODO: COMPARA A IMAGEM COM TODAS DO BANCO
            pass
        pass


if __name__ == '__main__':
    root = AuthenticatorRoot()
    root.mainloop()
