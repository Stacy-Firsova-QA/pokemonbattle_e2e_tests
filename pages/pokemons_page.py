import os

from locators.pokemons_list_locators import PokemonListLocators
from pages.base_page import BasePage

class PokemonsPage(BasePage):
    TITLE = "Битва Покемонов"

    # def __init__(self, driver):
    #     super().__init__(driver)

    def get_url(self):
        return f"{os.getenv('BASE_URL')}/"

    def should_be_loaded(self):
        self.find_element_visible(PokemonListLocators.trainer_card_id)

    def should_have_correct_url(self):
        self.should_have_url(self.get_url())

    def should_be_opened(self):
        self.should_be_loaded()
        self.should_have_correct_url()

    def open_trainer_page(self):
        self.click(PokemonListLocators.trainer_card_id)
