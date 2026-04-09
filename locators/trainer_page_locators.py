from selenium.webdriver.common.by import By
from data.test_trainer_data import TEST_TRAINER_ID, TEST_TRAINER_NAME

class TrainerPageLocators:

    trainer_name = (By.XPATH, f"//h2[text()='{TEST_TRAINER_NAME}']")
    to_premium = (By.CSS_SELECTOR, "div[data-qa='premium']")
    beginning_icon_active = (By.CSS_SELECTOR, ".beginning-icon.active")