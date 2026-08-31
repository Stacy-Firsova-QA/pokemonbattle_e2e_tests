import allure

from locators.trainer_page_locators import TrainerPageLocators


@allure.title("Проверка верстки отдельного блока на странице тренера")
@allure.tag("TrainerPage")
@allure.description(
    "Проверка блока с информацией о тренере со скрытием объектов: кол-во покеболов, уровень, ачивки")
def test_screenshot_trainer_page(open_trainer_page, screenshot_test):
    trainer_page = open_trainer_page

    screenshot_test(
        driver=trainer_page.driver,
        name="trainer_info_card.png",
        element=TrainerPageLocators.trainer_info_block,
        mask=[
            TrainerPageLocators.pokeballs_number,
            TrainerPageLocators.pokeballs_list,
            TrainerPageLocators.level_number,
            TrainerPageLocators.level_list,
            TrainerPageLocators.achievements_all_icons,
        ],
        threshold=0.05,
    )
