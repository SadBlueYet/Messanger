
from user_input import input_integer
from verification import UserVerification
from user_data import UserData


class MainInterface:
    def __init__(self):

        self.verification = UserVerification()
        self.data = UserData()

    def user_interface(self):
        menu = ("[1] Регистрация\n"
                "[2] Логин"
                )
        while True:
            user_choice = input_integer(menu)
            if user_choice == 1:
                self.verification.registry()
            if user_choice == 2:
                self.verification.login()


def main():
    interface = MainInterface()
    interface.user_interface()


if __name__ == "__main__":
    main()
