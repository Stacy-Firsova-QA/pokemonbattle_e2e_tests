import random

import allure
import pytest

from data.payment_data import INVALID_CARD_DATE, INVALID_CARD_NUMBER
from helpers.premium_helpers import calculate_premium_price, check_premium_status
from pages.pokemons_page import PokemonsPage
from pages.premium_pages import PremiumPages


@allure.title("Покупка премиума: разные сценарии оплаты через csv")
@allure.description(
    "Проверка 3 видов csv: корректного, некорректного, с недостатком средств на счету")
@allure.tag("PremiumPages", "PokemonsPage")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.no_headless
@pytest.mark.ui
@pytest.mark.parametrize("card_csv, expected_result, expected_text", [
    ("125", "success", "Покупка прошла успешно"),
    ("126", "error", "При оплате произошла ошибка"),
    ("300", "error", "При оплате произошла ошибка"),
], ids=["success result", "error result: invalid csv",
        "error result: insufficient funds"])
def test_buy_premium_different_csv_values(prepare_for_buy_premium,
                                          open_premium_form_page, api_session,
                                          card_csv, expected_result,
                                          expected_text):
    premium_page = open_premium_form_page
    premium_page.enter_days()
    premium_page.go_to_payment_page()

    premium_page.should_be_premium_card_form_page()
    premium_page.fill_card_number_with_js()
    premium_page.fill_card_date()
    premium_page.should_hide_card_date_errors()
    premium_page.fill_card_csv(card_csv)
    premium_page.fill_card_name()
    premium_page.go_to_3ds_page()

    premium_page.should_be_3ds_page()
    premium_page.fill_secure_code()
    premium_page.confirm_payment()

    status = premium_page.should_show_premium_status()
    if expected_result == "success":
        assert expected_text in status.text
        premium_page.back_to_store()
        premium_page.should_show_success_premium()
        premium_page.back_to_main()
        pokemons_page = PokemonsPage(premium_page.driver)
        pokemons_page.should_be_opened()
        assert check_premium_status(api_session) is True

    else:
        assert expected_text in status.text
        premium_page.back_to_store()
        assert check_premium_status(api_session) is False


@allure.title("Проверка расчета стоимости Премиума: успешный сценарий")
@allure.description(
    "Проверка правильного расчета суммы при разных вариантах дней подписки")
@allure.tag("PremiumPages")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.no_headless
def test_calculate_premium_price(prepare_for_buy_premium,
                                 open_premium_form_page):
    days = (random.randint(1, 999))
    expected_price = calculate_premium_price(days)
    # как работает:
    # ":" - значит "дальше идут правила форматирования"
    # "," - значит "разделяй тысячи"
    expected_price_formatted = f"{expected_price:,}".replace(",", " ")

    open_premium_form_page.enter_days(str(days))
    price_premium = open_premium_form_page.should_show_price()
    assert expected_price_formatted in price_premium.text, "Сумма не соответствует ожидаемой"


@allure.title("Ввод невалидного номера карты для оплаты: негативный сценарий")
@allure.tag("PremiumPages")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.no_headless
def test_invalid_card_number(prepare_for_buy_premium,
                             open_premium_card_form_page):
    open_premium_card_form_page.fill_card_number_with_js(
        card_number=INVALID_CARD_NUMBER)
    open_premium_card_form_page.fill_card_date()
    open_premium_card_form_page.should_show_invalid_card_date_errors()
    open_premium_card_form_page.fill_card_csv()
    open_premium_card_form_page.fill_card_name()

    open_premium_card_form_page.should_show_invalid_card_number_errors()
    open_premium_card_form_page.should_show_disabled_submit_button()


@allure.title("Ввод невалидного срока карты для оплаты: негативный сценарий")
@allure.description("Проверка, что нельзя ввести дату в прошлом")
@allure.tag("PremiumPages")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.no_headless
def test_invalid_card_date(prepare_for_buy_premium,
                           open_premium_card_form_page):
    open_premium_card_form_page.fill_card_number_with_js()
    open_premium_card_form_page.fill_card_date(card_date=INVALID_CARD_DATE)

    open_premium_card_form_page.should_show_invalid_card_date_errors()

    open_premium_card_form_page.fill_card_csv()
    open_premium_card_form_page.fill_card_name()

    open_premium_card_form_page.should_show_disabled_submit_button()


@allure.title("Отмена премиума: успешный сценарий")
@allure.tag("TrainerPage", "PremiumPages")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.no_headless
@pytest.mark.ui
def test_cancel_premium_successfully(prepare_for_cancel_premium,
                                     open_trainer_page, api_session):
    open_trainer_page.go_to_premium_page()

    premium_page = PremiumPages(open_trainer_page.driver)
    premium_page.cancel_premium()
    premium_page.confirm_cancellation()

    premium_page.should_show_success_cancellation()
    premium_page.back_to_trainer_page_after_cancellation()

    open_trainer_page.should_be_opened()
    assert check_premium_status(api_session) is False
