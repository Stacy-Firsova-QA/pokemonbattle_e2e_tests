import os
from locators.login_page_locators import LoginPageLocators

from pages.base_page import BasePage


class LoginPage(BasePage):
    TITLE = "Битва Покемонов"

    # def __init__(self, driver):
    #     super().__init__(driver)

    def get_url(self):
        return f"{os.getenv('BASE_URL')}/login"

    def login(self, user: str | None = None, pwd: str | None = None):
        login_value = user or os.getenv("LOGIN")
        pwd_value = pwd or os.getenv("PASSWORD")

        # проверка на случай, если логин/пароль вообще не нашлись нигде
        if login_value is None:
            raise ValueError("LOGIN is not set")
        if pwd_value is None:
            raise ValueError("PASSWORD is not set")

        self.type(LoginPageLocators.login_input, login_value, "Поле ввода логина")
        self.type(LoginPageLocators.password_input, pwd_value, "Поле ввода пароля")
        self.click(LoginPageLocators.login_button, "Кнопка входа")
