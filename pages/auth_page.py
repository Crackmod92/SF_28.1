from .base_page import BasePage
from .locators import AuthLocators


class AuthPage(BasePage):

    def __init__(self, driver, timeout=10,):
        super().__init__(driver, timeout)
        url = 'https://b2c.passport.rt.ru'
        # driver.maximize_window()
        driver.get(url)

        self.tab_phone = driver.find_element(*AuthLocators.tab_phone)
        self.active_tab_phone = driver.find_element(*AuthLocators.active_tab_phone)
        self.tab_email = driver.find_element(*AuthLocators.tab_email)
        self.email = driver.find_element(*AuthLocators.auth_email)
        self.pass_email = driver.find_element(*AuthLocators.auth_pass_email)
        self.btn_enter = driver.find_element(*AuthLocators.auth_btn_enter)
        self.tab_login = driver.find_element(*AuthLocators.tab_login)
        self.login = driver.find_element(*AuthLocators.auth_login)
        self.pass_log = driver.find_element(*AuthLocators.auth_pass_log)
        self.tab_ls = driver.find_element(*AuthLocators.tab_ls)
        self.placeholder_name = driver.find_element(*AuthLocators.placeholder_name)
        self.forgot_password_link = driver.find_element(*AuthLocators.forgot_password_link)
        self.register_link = driver.find_element(*AuthLocators.register_link)
        self.page_right = driver.find_element(*AuthLocators.page_right)
        self.page_left = driver.find_element(*AuthLocators.page_left)
        self.card_of_auth = driver.find_element(*AuthLocators.card_of_auth)
        self.menu_tab = driver.find_element(*AuthLocators.menu_tab)

    def find_other_element(self, by, location):
        return self.driver.find_element(by, location)