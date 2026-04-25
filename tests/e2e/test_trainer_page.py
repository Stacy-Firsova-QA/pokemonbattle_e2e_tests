import allure
from pages.trainer_page import TrainerPage
from pages.premium_pages import PremiumPages

@allure.title("Проверка активной ачивки 'Начало большого пути'")
def test_check_achiev_beginning_icon_active(open_trainer_page):
    open_trainer_page.should_show_active_beginning_icon()

@allure.title("Тест на переход со страницы тренера на страницу оформления премиума")
def test_from_trainer_page_to_premium(open_trainer_page):
    open_trainer_page.go_to_premium_page()

    premium_form_page = PremiumPages(open_trainer_page.driver)
    premium_form_page.should_be_opened()


