from settings import Settings

incor_email = [Settings.invalid_email, Settings.empty_email]
incor_passw = [Settings.invalid_password, Settings.empty_password]

valid_first_last_name = [
    Settings.russian_characters * 2,
    Settings.russian_characters * 3,
    Settings.russian_characters * 15,
    Settings.russian_characters * 29,
    Settings.russian_characters * 30
]

invalid_first_last_name = [
    Settings.russian_characters * 1,
    Settings.russian_characters * 100,
    Settings.russian_characters * 256,
    Settings.empty,
    Settings.numbers,
    Settings.latin_characters,
    Settings.special_symbols
]

valid_password = [
    Settings.password_7chars,
    Settings.password_10chars,
    Settings.password_16chars
]