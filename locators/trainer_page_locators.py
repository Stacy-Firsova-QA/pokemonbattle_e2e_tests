from selenium.webdriver.common.by import By
from data.test_trainer_data import TEST_TRAINER_ID, TEST_TRAINER_NAME

class TrainerPageLocators:

    trainer_name = (By.XPATH, f"//h2[text()='{TEST_TRAINER_NAME}']")