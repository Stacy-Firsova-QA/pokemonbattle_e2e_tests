import allure
import pytest

from pages.pokemons_page import PokemonsPage
from pages.trainer_page import TrainerPage


@allure.title("Проверка перехода с главной страницы на страницу тренера")
@allure.description("Проверка редиректа с главной страницы (список покемонов) на страницу тренера по кнопке")
@allure.tag("TrainerPage", "PokemonsPage")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.no_headless
def test_from_main_to_trainer_page(authorized_user):
    pokemons_page = PokemonsPage(authorized_user)
    pokemons_page.should_be_opened()
    pokemons_page.open_trainer_page()

    trainer_page = TrainerPage(authorized_user)
    trainer_page.should_be_opened()




