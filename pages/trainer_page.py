import os

from pages.base_page import BasePage
from locators.trainer_page_locators import TrainerPageLocators
from data.test_trainer_data import TEST_TRAINER_ID


class TrainerPage(BasePage):
    # def __init__(self, driver):
    #     super().__init__(driver)

    def get_url(self):
        return f"{os.getenv('BASE_URL')}/trainer/{TEST_TRAINER_ID}"

    def should_be_loaded(self):
        self.find_element_visible(TrainerPageLocators.trainer_name)

    def should_have_correct_url(self):
        self.should_have_url(self.get_url())

    def should_be_opened(self):
        self.should_be_loaded()
        self.should_have_correct_url()

    def go_to_premium_page(self):
        self.click(TrainerPageLocators.to_premium)

    def should_show_active_beginning_icon(self):
        # чуть попозже можно реализовать полную логику, если, допустим, у тренера нет подготовленной активной ачивки
        self.find_element_visible(TrainerPageLocators.beginning_icon_active)
