from app.common import helpers


def row(text):

    chars = helpers.convert_string_character_code(
        text.upper()
    )

    while len(chars) < 22:

        chars.append(0)

    return chars[:22]