from selenium.webdriver.common.by import By
from data.test_trainer_data import TEST_TRAINER_ID, TEST_TRAINER_NAME


class TrainerPageLocators:
    trainer_name = (By.XPATH, f"//h2[text()='{TEST_TRAINER_NAME}']")
    to_premium = (By.CSS_SELECTOR, "div[data-qa='premium']")
    beginning_icon_active = (By.CSS_SELECTOR, ".beginning-icon.active")
    # элементы внутри блока с информацией по тренеру и сам блок
    trainer_info_block = (By.CSS_SELECTOR,
                          ".single_page_body_content_inner > .single_page_body_content_inner_top")
    pokeballs_number = (By.XPATH,
                        "//span[text()='Покеболы']/following-sibling::span[1]")
    pokeballs_list = (By.XPATH,
                      "//span[text()='Покеболы']/following-sibling::ul[1]")
    level_number = (By.XPATH,
                    "//span[text()='Уровень']/following-sibling::span[1]")
    level_list = (By.XPATH,
                  "//span[text()='Уровень']/following-sibling::ul[1]")
    achievements_all_icons = (By.XPATH, "//div[@class='achievements']")
