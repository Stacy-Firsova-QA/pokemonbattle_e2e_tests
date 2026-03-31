import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.pokemons_list_locators import PokemonListLocators
from locators.trainer_page_locators import TrainerPageLocators
from data.test_trainer_data import TEST_TRAINER_ID

def test_authorization_successfully(driver, authorization):
    driver.implicitly_wait(1)

    driver.find_element(*PokemonListLocators.trainer_card_id)
    assert driver.current_url == "https://pokemonbattle.ru/"

def test_from_main_to_trainer_page(driver, authorization):
    wait = WebDriverWait(driver, 1)

    trainer_card = wait.until(EC.element_to_be_clickable(PokemonListLocators.trainer_card_id))
    trainer_card.click()

    trainer_name = wait.until(EC.visibility_of_element_located(TrainerPageLocators.trainer_name))
    assert driver.current_url == f"https://pokemonbattle.ru/trainer/{TEST_TRAINER_ID}"


