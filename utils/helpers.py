import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_random_address():
    addresses = [
        "улица Тверская, 7",
        "улица Арбат, 25",
        "проспект Мира, 119",
        "Ленинский проспект, 32",
        "улица Новый Арбат, 15"
    ]
    return random.choice(addresses)