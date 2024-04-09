import random


MAX_LENGTH_RANDOM_CONFIRMATION_CODE = 6


def generate_random_confirmation_code() -> str:
    """
    This function generates a random confirmation code, based on the ASCII table values of a-z, A-Z, 0-9
    :return: str
    """

    available_values = (
        range(65, 90 + 1),
        range(97, 122 + 1),
        range(48, 57 + 1),
    )

    password = ''

    for _ in range(MAX_LENGTH_RANDOM_CONFIRMATION_CODE):
        values_to_chose_from = available_values[random.choice([0, 1])]
        chosen_value = random.choice(values_to_chose_from)
        password += chr(chosen_value)

    return password
