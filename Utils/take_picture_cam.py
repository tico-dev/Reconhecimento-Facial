from tkinter import *
from tkinter import ttk

from Utils.general import IMAGES_PATH

import os

from PIL import ImageTk, Image
import cv2


class UserImage:
    def __init__(self):
        self.user_image = None

    def set_user_image(self, user_image):
        self.user_image = user_image

    def get_user_image(self):
        return self.user_image


class TakePictureRoot(Toplevel):
    def __init__(self):
        super(TakePictureRoot, self).__init__()
        self.title("Fotografar usuário")  # Define o título da janela
        self.geometry("600x600")  # Dimensões da janela
        self.resizable(False, False)  # Desliga a função de redimensionar a janela (X, Y)

        self.user_image_class = UserImage()

        # -------------------------------- Variáveis -------------------------------- #
        # Referência da camera padrão do sistema
        self.cap = cv2.VideoCapture(0)
        # Tarefa da thread
        self._job = None
        # --------------------------------------------------------------------------- #

        # Display imagem do usuário:
        self.labelFrameImageDisplay = ttk.LabelFrame(self, text="Imagem da camera:")
        self.labelFrameImageDisplay.pack(side=TOP, pady=20)

        # Label rodapé:
        self.labelFooter = ttk.LabelFrame(self)
        self.labelFooter.pack(side=BOTTOM, expand=1)

        self.image_display = Label(self.labelFrameImageDisplay, image='')
        self.image_display.image = ''
        self.image_display.pack()
        self._image_display()

        # Botão de tirar screenshot:
        self.labelScreenshotButton = Label(self.labelFooter)
        self.labelScreenshotButton.pack(side=LEFT, expand=1, padx=20)
        self._screenshot_button()

        # Botão de enviar:
        self.labelFrameSubmitButton = Label(self.labelFooter)
        self.labelFrameSubmitButton.pack(side=RIGHT, expand=1, padx=20)
        self._submit_button()

    def _image_display(self):
        self.image_display.configure(image='')
        self.image_display.image = ''
        _, self._frame = self.cap.read()
        self._cv2image = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(self._cv2image)
        render = ImageTk.PhotoImage(img)
        self.image_display.configure(image=render)
        self.image_display.image = render

        self._job = self.labelFrameImageDisplay.after(10, self._image_display)

    def _screenshot_button(self):
        self.screenshot_button = Button(self.labelScreenshotButton, text="Tirar screenshot", command=self._screenshot)
        self.screenshot_button.pack(anchor=W)

    def _screenshot(self):
        if self._job:
            self.labelFrameImageDisplay.after_cancel(self._job)
            self._job = None
            self.screenshot_button.configure(text="voltar a filmar")
            if not cv2.imwrite(os.path.join(IMAGES_PATH, 'user_picture.jpg'), self._frame):
                raise Exception("Não conseguiu salvar a imagem.")

            if self.submit_button["state"] == NORMAL:
                self.submit_button["state"] = DISABLED
            else:
                self.submit_button["state"] = NORMAL

            return
        self._job = self.labelFrameImageDisplay.after(1, self._image_display)
        self.screenshot_button.configure(text="Tirar foto")

    def _submit_button(self):
        self.submit_button = Button(self.labelFrameSubmitButton, text="Usar essa foto", command=self.submit)
        self.submit_button['state'] = DISABLED
        self.submit_button.pack(anchor=E)

    def submit(self):
        self.user_image_class.set_user_image(os.path.join(IMAGES_PATH, 'user_picture.jpg'))
        self.cap.release()
        self.destroy()


def get_user_picture():
    root = TakePictureRoot()
    root.wait_window()
    return root.user_image_class.get_user_image()
