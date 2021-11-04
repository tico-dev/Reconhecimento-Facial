from Graphical_Interfaces.user_registration import RegisterRoot
from Graphical_Interfaces.user_authentication import AuthenticationRoot
from time import sleep


if __name__ == '__main__':
    print('DEPOIS IREI FAZER UMA INTERFACE SIMPLEZINHA PARA ISSO!\nPor enquanto estou focando em fazer funcionar, '
          'posteriormente deixarei mais bonito (melhorarei UI/UX)')

    while True:
        print('---' * 15)

        try:
            decision = int(input('O que deseja fazer:\n1- Cadastrar um novo usuário.\n2- Entrar em minha conta.\n'
                             '3- finalizar o programa.\n[user]: '))
        except ValueError:
            print("Por favor, digite apenas números.")
            sleep(1)
            continue

        if decision not in (1, 2, 3):
            print('input invalido!')
        else:
            if decision == 1:
                print("provavelmente uma janela para cadastro se abriu em segundo plano")
                registerApp = RegisterRoot()
                registerApp.mainloop()
                sleep(2)
                continue
            elif decision == 2:
                print("provavelmente uma janela para autenticação se abriu em segundo plano")
                autheticationApp = AuthenticationRoot()
                autheticationApp.mainloop()
                continue
            elif decision == 3:
                print('finalizando programa...')
                sleep(2)
                exit()
