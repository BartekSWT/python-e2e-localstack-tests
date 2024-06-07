from faker import Faker

from api.data.register import User

fake = Faker()


def generate_username() -> str:
    username = fake.user_name()
    attempts = 0
    while len(username) < 4 and attempts < 10:
        username = fake.user_name()
        attempts += 1
    return username


def generate_password() -> str:
    password = fake.password()
    attempts = 0
    while len(password) < 4 and attempts < 10:
        password = fake.password()
        attempts += 1
    return password


def generate_first_name() -> str:
    first_name = fake.first_name()
    attempts = 0
    while len(first_name) < 4 and attempts < 10:
        first_name = fake.first_name()
        attempts += 1
    return first_name


def generate_last_name() -> str:
    last_name = fake.last_name()
    attempts = 0
    while len(last_name) < 4 and attempts < 10:
        last_name = fake.last_name()
        attempts += 1
    return last_name


def get_random_user() -> User:
    username = generate_username()
    password = generate_password()
    first_name = generate_first_name()
    last_name = generate_last_name()

    return User(
        username=username,
        password=password,
        email=fake.email(),
        firstName=first_name,
        lastName=last_name,
        roles=["ROLE_ADMIN", "ROLE_CLIENT"],
    )
