import pytest
import os
from selenium import webdriver
from selenium.webdriver import chrome
from dotenv import load_dotenv
from locators.login_page_locators import LoginPageLocators
from locators.pokemons_list_locators import PokemonListLocators
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

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



