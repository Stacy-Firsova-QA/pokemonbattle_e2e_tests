import pytest
import os
from selenium import webdriver
from locators.login_page_locators import LoginPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.pokemons_list_locators import PokemonListLocators
from locators.trainer_page_locators import TrainerPageLocators
from locators.payment_forms_locators import PremiumBuyFormLocators, PaymentCardFormLocators
from data.test_trainer_data import TEST_TRAINER_ID
from pages.trainer_page import TrainerPage
from pages.login_page import LoginPage
from pages.pokemons_page import PokemonsPage
from pages.premium_pages import PremiumPages

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture()
def authorized_user(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login()

    return driver

@pytest.fixture()
def open_trainer_page(authorized_user):
    pokemons_page = PokemonsPage(authorized_user)
    pokemons_page.should_be_opened()
    pokemons_page.open_trainer_page()

    trainer_page = TrainerPage(authorized_user)
    trainer_page.should_be_opened()

    return trainer_page

@pytest.fixture()
def open_premium_form_page(open_trainer_page):
    open_trainer_page.go_to_premium_page()

    premium_form_page = PremiumPages(open_trainer_page.driver)
    premium_form_page.should_be_opened()

    return premium_form_page

@pytest.fixture()
def open_premium_card_form_page(open_premium_form_page):
    open_premium_form_page.enter_days()
    open_premium_form_page.go_to_payment_page()
    open_premium_form_page.should_be_premium_card_form_page()
    open_premium_form_page.should_have_url(f"{os.getenv('BASE_URL')}/payment/0")

    return open_premium_form_page

