
def input_username():
    username = input("Введите имя пользователя\n>> ")
    return username


def input_password():
    password = input("Введите пароль\n>> ")
    return password


def input_telephone_number():
    telephone_number = input("Введите номер телефона\n>> ")
    return telephone_number


def input_integer(text):
    while True:
        try:
            user_choice = int(input(f"{text}\n>> "))
            return user_choice
        except ValueError as e:
            print(e)
            continue
