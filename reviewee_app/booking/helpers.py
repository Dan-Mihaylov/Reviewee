import random


def generate_random_confirmation_code(length: int) -> str:
    """
    This function generates a random confirmation code, based on the ASCII table values of a-z, A-Z, 0-9
    :param length: length of the confirmation code you want to generate
    :return: str
    """

    available_values = (
        range(65, 90 + 1),
        range(97, 122 + 1),
        range(48, 57 + 1),
    )

    password = ''

    for _ in range(length):
        values_to_chose_from = available_values[random.choice([0, 1])]
        chosen_value = random.choice(values_to_chose_from)
        password += chr(chosen_value)

    return password

