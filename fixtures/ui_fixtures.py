import os

import pytest
from selenium import webdriver

from pages.login_page import LoginPage
from pages.pokemons_page import PokemonsPage
from pages.premium_pages import PremiumPages
from pages.trainer_page import TrainerPage


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1200)
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

