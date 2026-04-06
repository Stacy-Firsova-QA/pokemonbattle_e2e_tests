import pytest
import os
from selenium import webdriver
from locators.login_page_locators import LoginPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.pokemons_list_locators import PokemonListLocators
from locators.trainer_page_locators import TrainerPageLocators
from locators.payment_forms_locators import PremiumBuyFormLocators
from data.test_trainer_data import TEST_TRAINER_ID

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture()
def authorization(driver):
    driver.get(os.getenv("BASE_URL"))

    login_input = driver.find_element(*LoginPageLocators.login_input)
    login_input.send_keys(os.getenv("LOGIN"))
    password_input = driver.find_element(*LoginPageLocators.password_input)
    password_input.send_keys(os.getenv("PASSWORD"))

    login_button = driver.find_element(*LoginPageLocators.login_button)
    login_button.click()

    yield driver

@pytest.fixture()
def open_trainer_page(authorization):
    wait = WebDriverWait(authorization, 3)

    trainer_card = wait.until(EC.element_to_be_clickable(PokemonListLocators.trainer_card_id))
    trainer_card.click()

    wait.until(EC.visibility_of_element_located(TrainerPageLocators.trainer_name))
    assert authorization.current_url == f"{os.getenv('BASE_URL')}/trainer/{TEST_TRAINER_ID}"

    yield authorization

@pytest.fixture()
def open_premium_page(open_trainer_page):
    wait = WebDriverWait(open_trainer_page, 2)

    premium_tab = wait.until(EC.element_to_be_clickable(TrainerPageLocators.to_premium))
    premium_tab.click()

    wait.until(EC.visibility_of_element_located(PremiumBuyFormLocators.profile_title))
    assert open_trainer_page.current_url == os.getenv("BASE_URL") + "/premium"

    yield open_trainer_page