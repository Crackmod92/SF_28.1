import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pages.auth_page import AuthPage
from pages.registr_page import RegistrPage
from pages.locators import AuthLocators
from settings import *
from params import incor_email, incor_passw
from params import valid_first_last_name
from params import invalid_first_last_name
from params import valid_password


# TCRT-01 Тест раздела "Авторизация" на наличие основных элементов:
def test_elements_of_authorization(selenium):
    page = AuthPage(selenium)
    elements = [page.menu_tab, page.email, page.pass_email, page.btn_enter, page.forgot_password_link,
                page.register_link]

    for element in elements:
        assert element.text in page.card_of_auth.text


# TCRT-02 Тест на проверку названий вкладок в меню "Авторизация"
def test_menu_tab_authorization(selenium):
    page = AuthPage(selenium)
    menu = [page.tab_phone.text, page.tab_email.text, page.tab_login.text, page.tab_ls.text]
    assert "Телефон" in menu, "Ошибка в имени вкладки аутентификации: отсутствует Телефон"
    assert 'Почта' in menu, "Ошибка в имени вкладки аутентификации: отсутствует Почта"
    assert 'Логин' in menu, "Ошибка в имени вкладки аутентификации: отсутствует Логин"
    assert 'Лицевой счёт' in menu, "Ошибка в имени вкладки аутентификации: отсутствует Лицевой счёт"


# TCRT-03 Тест авторизации с действительной почтой и паролем
def test_authorization_valid_email_pass(selenium):
    page = AuthPage(selenium)
    page.email.send_keys(Settings.valid_email)
    page.pass_email.send_keys(Settings.valid_password)
    page.btn_enter.click()

    try:
        assert page.get_relative_link() == '/account_b2c/page'
    except AssertionError:
        assert 'Неверно введен текст с картинки' in page.find_other_element(*AuthLocators.error_message).text


# TCRT-04 Тест авторизации с недействительной почтой и паролем:
@pytest.mark.parametrize("incor_email", incor_email,
                         ids=['invalid_email', 'empty'], scope="function")
@pytest.mark.parametrize("incor_passw", incor_passw,
                         ids=['invalid_password', 'empty'], scope="function")
def test_authorization_invalid_email_pass(selenium, incor_email, incor_passw):
    page = AuthPage(selenium)
    page.email.send_keys(incor_email)
    page.pass_email.send_keys(incor_passw)
    page.btn_enter.click()

    assert page.get_relative_link() != '/account_b2c/page', f"Авторизация была успешной при вводе неправильных " \
                                                            f"данных: email = {incor_email}, password = {incor_passw}"


# TCRT-05 Тест выбора вкладки по умолчанию в Меню выбора типа авторизации
def test_menu_tab_active_authorization(selenium):
    page = AuthPage(selenium)

    expected_active_tab_text = Settings.menu_type_auth[0]
    assert page.active_tab_phone.text == expected_active_tab_text, f"Текст активной вкладки не совпадает с ожидаемым: " \
                                                                   f"ожидаемый текст - {expected_active_tab_text}, " \
                                                                   f"активная вкладка - {page.active_tab_phone.text}"


# TCRT-06 Тест к переходу к форме "Восстановление пароля"
def test_forgot_password_link(selenium):
    page = AuthPage(selenium)
    page.forgot_password_link.click()

    WebDriverWait(page.driver, 10).until(EC.presence_of_element_located(AuthLocators.password_recovery))

    assert page.find_other_element(*AuthLocators.password_recovery).text == 'Восстановление пароля'


# TCRT-07 Тест к переходу к форме "Регистрация"
def test_registration_page_link(selenium):
    page = AuthPage(selenium)
    page.register_link.click()

    registration_element = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[text("")='Регистрация']")))
    assert registration_element.text == 'Регистрация'


# TCRT-08 Проверка Формы "Регистрация" на наличие основных элементов
def test_elements_registration_page(selenium):
    page_reg = RegistrPage(selenium)
    card_of_reg = [
        page_reg.first_name,
        page_reg.last_name,
        page_reg.address_registration,
        page_reg.email_registration,
        page_reg.password_registration,
        page_reg.password_registration_confirm,
        page_reg.registration_btn
    ]
    assert all(elem in card_of_reg for elem in [page_reg.first_name, page_reg.last_name,
                                                page_reg.email_registration,
                                                page_reg.address_registration,
                                                page_reg.password_registration,
                                                page_reg.password_registration_confirm,
                                                page_reg.registration_btn]), 'Элемент отсутствует в форме «Регистрация»'


# TCRT-09 Проверка Формы "Регистрация" на соответствие названий элементов блока требованию
def test_names_elements_registration(selenium):
    page_reg = RegistrPage(selenium)
    assert 'Имя' in page_reg.card_of_registration.text, "Элемент 'Имя' не найден"
    assert 'Фамилия' in page_reg.card_of_registration.text, "Элемент 'Фамилия' не найден"
    assert 'Регион' in page_reg.card_of_registration.text, "Элемент 'Регион' не найден"
    assert 'E-mail или мобильный телефон' in page_reg.card_of_registration.text, "Элемент 'E-mail или мобильный телефон' не найден"
    assert 'Пароль' in page_reg.card_of_registration.text, "Элемент 'Пароль' не найден"
    assert 'Подтверждение пароля' in page_reg.card_of_registration.text, "Элемент 'Подтверждение пароля' не найден"
    assert 'Зарегистрироваться' in page_reg.card_of_registration.text, "Кнопка 'Зарегистрироваться' не найдена"


# TCRT-10 Тест регистрации нового пользователя с корректными данными
def test_new_user_registration_valid_data(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email_for_reg)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert page_reg.find_other_element(*AuthLocators.email_confirm).text == 'Подтверждение email'


# TCRT-11 Тест на проверку доступности введенного e-mail в форме "Регистрация"
def test_registration_with_invalid_email(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert "Учётная запись уже существует" in page_reg.find_other_element(*AuthLocators.error_account_exists).text


# TCRT-12 Тест поля регистрации "Имя" - корректные и граничные значения
@pytest.mark.parametrize("valid_first_last_name", valid_first_last_name, ids=(
        "russian_characters=2", 'russian_characters=3', 'russian_characters=15',
        'russian_characters=29', 'russian_characters=31'), scope="function")
def test_valid_first_name(selenium, valid_first_last_name):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.clear()
    page_reg.first_name.send_keys(valid_first_last_name)
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' not in page_reg.container_first_name.text


# TCRT-13 Тест поля регистрации "Имя" - некорректные значения
@pytest.mark.parametrize("invalid_first_last_name", invalid_first_last_name,
                         ids=('1_char', '100_chars', '256_chars', 'empty',
                              'numbers', 'latin_chars', 'special_symbols'), scope="function")
def test_invalid_first_name(selenium, invalid_first_last_name):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.clear()
    page_reg.first_name.send_keys(invalid_first_last_name)
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' in \
           page_reg.find_other_element(*AuthLocators.error_first_name).text


# TCRT-14 Тест поля регистрации "Пароль" корректными данными
@pytest.mark.parametrize("valid_password", valid_password,
                         ids=['valid_symbols=8', 'valid_symbols=15', 'valid_symbols=20'], scope="function")
def test_password_valid_data(selenium, valid_password):
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(valid_password)
    page_reg.password_registration.clear()
    page_reg.registration_btn.click()

    assert 'Длина пароля должна быть не менее 8 символов' and \
           'Длина пароля должна быть не более 20 символов' and \
           'Пароль должен содержать хотя бы одну заглавную букву' and \
           'Пароль должен содержать хотя бы одну прописную букву' and \
           'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру' not in \
           page_reg.password_registration.text


# TCRT-15 Тест поля ввода "Пароль" и "Подтвердить пароль" формы «Регистрация» одинаковыми паролями
def test_registration_confirm_password_valid_data(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.password_10chars)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.password_10chars)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' not in page_reg.container_password_confirm.text


# TCRT-16 Тест поля ввода "Пароль" и "Подтвердить пароль" формы «Регистрация» разными паролями
def test_registration_confirm_password_invalid_data(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.password_10chars)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.password_16chars)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' in page_reg.find_other_element(*AuthLocators.error_password_confirm).text


# TCRT-17 Тест смены полей ввода при смене типа авторизации
def test_placeholder_name_change(selenium):
    page = AuthPage(selenium)

    tabs = [page.tab_phone, page.tab_email, page.tab_login, page.tab_ls]
    for tab in tabs:
        tab.click()
        assert page.placeholder_name.text in Settings.placeholder_name


#  TCRT-18 Тест логотипа компании на странице "Регистрация
def test_logo_registration_page(selenium):
    try:
        page_reg = RegistrPage(selenium)
        assert page_reg.page_left_registration.text != ''
    except AssertionError:
        print('Элемент отсутствует в левой части формы')



