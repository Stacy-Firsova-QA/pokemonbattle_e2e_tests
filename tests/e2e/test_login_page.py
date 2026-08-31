import allure
import pytest

from pages.login_page import LoginPage
from pages.pokemons_page import PokemonsPage


@allure.title("Проверка успешной авторизации")
@allure.description(
    "Проверка авторизации неавторизованного пользователя и перехода на главную (список покемонов)")
@allure.tag("LoginPage", "PokemonsPage")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.no_headless
@pytest.mark.ui
def test_authorize_user(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login()

    pokemons_page = PokemonsPage(driver)
    pokemons_page.should_be_loaded()
    pokemons_page.should_have_correct_url()
