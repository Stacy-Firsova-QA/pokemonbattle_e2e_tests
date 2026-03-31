from selenium.webdriver.common.by import By
from data.test_trainer_data import TEST_TRAINER_ID

class PokemonListLocators:

    trainer_card_id = (By.XPATH, f"//div[@class='header_card_trainer_id_num' and text()='{TEST_TRAINER_ID}']")