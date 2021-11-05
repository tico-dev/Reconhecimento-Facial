from tkinter import *
from PIL import ImageTk, Image
import cv2


class AuthenticatorRoot(Tk):
    def __init__(self):
        super(AuthenticatorRoot, self).__init__()
        self.title("Identificação de usuário")  # Define o título da janela
        self.geometry("600x600")  # Dimensões da janela
        self.resizable(False, False)  # Desliga a função de redimensionar a janela (X, Y)

        # Camera
        self.cap = cv2.VideoCapture(0)
        # Tarefa da thread
        self._job = None

        # Display imagem do usuário:
        self.labelFrameImageDisplay = LabelFrame(self, text="Imagem da camera:", bg="white")
        self.labelFrameImageDisplay.pack(side=TOP, expand=1, pady=20)
        
        # Botão de tirar screenshot:
        self.labelScreenshotButton = Label(self)
        self.labelScreenshotButton.pack(side=BOTTOM, expand=1, padx=20, pady=20)
        self._screenshot_button()

        self.image_display = Label(self.labelFrameImageDisplay, image='')
        self.image_display.image = ''
        self.image_display.pack()
        self._image_display()

        # Botão de enviar:
        self.labelFrameSubmitButton = Label(self)
        self.labelFrameSubmitButton.pack(side=BOTTOM, expand=1, padx=20, pady=20, anchor=W)
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
            cv2.imwrite("screenshot2.jpg", self._frame)
            return
        self._job = self.labelFrameImageDisplay.after(1, self._image_display)
        self.screenshot_button.configure(text="Tirar screenshot")

    def _submit_button(self):
        self.submit_button = Button(self.labelFrameSubmitButton, text="Cadastrar usuário", command=self.submit)
        self.submit_button.pack(anchor=W)

    def submit(self):
        pass
        # TODO SALVA A IMAGEM E COMPARA COM TODAS PRESENTES NO BANCO

if __name__ == "__main__":
    root = AuthenticatorRoot()
    root.mainloop()
    root.cap.release()