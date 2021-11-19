from Graphical_Interfaces.user_registration import RegisterRoot
from Graphical_Interfaces.user_authentication import Authenticator
from Graphical_Interfaces.user_authenticated import AuthenticatedRoot

from Database.DBConnector import Database
from Utils.general import DATABASE_FILE_PATH, User

if __name__ == '__main__':
    db = Database(DATABASE_FILE_PATH)
    while True:
        print('---' * 15)

        try:
            decision = int(input('O que deseja fazer:\n1- Cadastrar um novo usuário.\n2- Entrar em minha conta.\n'
                             '3- finalizar o programa.\n[user]: '))
        except ValueError:
            print("Por favor, digite apenas números.")
            continue

        if decision not in (1, 2, 3):
            print('input invalido!')
        else:
            if decision == 1:
                print("provavelmente uma janela para cadastro se abriu em segundo plano")
                registerApp = RegisterRoot()
                while not registerApp.finished:
                    registerApp.update()
                registerApp.destroy()
                continue

            elif decision == 2:
                print("provavelmente uma janela para autenticação se abriu em segundo plano")
                AuthenticatorApp = Authenticator()
                result = AuthenticatorApp.identify_user()
                if result:
                    userdata = db.get_user_by_name(result)
                    user = User(userdata[0], userdata[1], userdata[2], userdata[3], userdata[4], userdata[5])
                    print(user.show_values())

                    AuthenticatedUser = AuthenticatedRoot(user)
                    while not AuthenticatedUser.finished:
                        AuthenticatedUser.update()
                    AuthenticatedUser.destroy()
                continue

            elif decision == 3:
                print('finalizando programa...')
                exit()
