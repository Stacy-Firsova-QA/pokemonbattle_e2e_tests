import allure
import pytest

from data.payment_data import (
    CARD_CSV,
    CARD_DATE,
    CARD_NAME,
    CARD_NUMBER,
    INVALID_CARD_DATE,
    INVALID_CARD_NUMBER,
)
from locators.payment_forms_locators import (
    PaymentCardFormLocators,
    PremiumBuyFormLocators,
)


@allure.title("Проверка верстки формы для выбора премиум")
@allure.description("Проверка верстки для всех диапазонов и скидок для них")
@allure.tag("PremiumPages")
@pytest.mark.parametrize("days, period_name", [
    (20, "lt_30_days"),
    (50, "from_30_to_180_days"),
    (230, "from_180_to_365_days"),
    (379, "gt_365_days"),
])
def test_screenshot_premium_form_page(prepare_for_buy_premium,
                                      open_premium_form_page, screenshot_test,
                                      days, period_name):
    premium_form_page = open_premium_form_page
    premium_form_page.enter_days(str(days))
    premium_form_page.wait_cost_days_visible()
    premium_form_page.scroll_to_premium_form()

    screenshot_test(
        driver=premium_form_page.driver,
        name=f"premium_form_for_{period_name}.png",
        element=PremiumBuyFormLocators.main_form,
        threshold=0.05,
    )


@allure.title("Проверка верстки формы оплаты")
@allure.description(
    "Проверка верстки форм: пустая форма, заполненная форма, неверный номер карты, неверный срок карты")
@allure.tag("PremiumPages")
@pytest.mark.parametrize(
    "card_number, card_date, card_csv, card_name, form_name", [
        (None, None, None, None, "empty_form"),
        (CARD_NUMBER, CARD_DATE, CARD_CSV, CARD_NAME, "correct_form"),
        (INVALID_CARD_NUMBER, None, None, None, "invalid_card_number"),
        (None, INVALID_CARD_DATE, None, None, "invalid_card_date")],
    ids=["empty_form", "correct_form", "Invalid_card_number",
         "Invalid_card_date"])
def test_screenshot_premium_card_form_page(
        prepare_for_buy_premium,
        open_premium_card_form_page,
        screenshot_test,
        card_number,
        card_date,
        card_csv,
        card_name,
        form_name
):
    premium_card_form_page = open_premium_card_form_page

    if form_name == "empty_form":
        pass

    elif form_name == "correct_form":
        premium_card_form_page.fill_card_form(
            card_number=card_number,
            card_date=card_date,
            card_csv=card_csv,
            card_name=card_name
        )
        premium_card_form_page.blur_active_elements()
        premium_card_form_page.should_hide_card_date_errors()
        premium_card_form_page.should_submit_button_be_active()

    elif form_name == "invalid_card_number":
        premium_card_form_page.fill_card_number(card_number=card_number)
        premium_card_form_page.wait_number_input_errors_visible()
        premium_card_form_page.should_show_disabled_submit_button()

    elif form_name == "invalid_card_date":
        premium_card_form_page.fill_card_form(
            card_number=card_number,
            card_date=card_date,
            card_csv=card_csv,
            card_name=card_name
        )
        premium_card_form_page.wait_date_input_errors_visible()
        premium_card_form_page.should_show_disabled_submit_button()

    screenshot_test(
        driver=premium_card_form_page.driver,
        name=f"premium_card_form_{form_name}.png",
        element=PaymentCardFormLocators.payment_form,
        threshold=0.05,
    )
