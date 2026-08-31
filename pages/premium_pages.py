import os
from pages.base_page import BasePage
from locators.payment_forms_locators import PremiumBuyFormLocators, \
    PaymentCardFormLocators, ConfirmationPaymentFormLocators, \
    PaymentSuccessLocators, PremiumSuccessLocators, CancelPremiumLocators
from data.payment_data import CARD_NUMBER, CARD_CSV, CARD_DATE, CARD_NAME, \
    SECURE_CODE


class PremiumPages(BasePage):

    # def __init__(self, driver):
    #     super().__init__(driver)

    # def open_page(self):
    #     self.open(self.URL)

    def get_url(self):
        return f"{os.getenv('BASE_URL')}/premium"

    def should_be_loaded(self):
        self.find_element_visible(PremiumBuyFormLocators.profile_title)

    def should_have_correct_url(self):
        self.should_have_url(self.get_url())

    def should_be_opened(self):
        self.should_be_loaded()
        self.should_have_correct_url()

    def enter_days(self, days="1"):
        self.type(PremiumBuyFormLocators.days_input, days)

    def wait_cost_days_visible(
            self):  # дожидаемся что после ввода дней скидка полностью видна (для скриншот-теста)
        self.wait.until(
            lambda d: d.find_element(
                *PremiumBuyFormLocators.cost_days).get_attribute(
                "style").strip() == ""
        )

    def wait_date_input_errors_visible(self):
        self.wait.until(
            lambda d: d.find_element(
                *PaymentCardFormLocators.error_date_input).get_attribute(
                "style").strip() == ""
        )
        self.wait.until(
            lambda d: d.find_element(
                *PaymentCardFormLocators.error_date_input_text).get_attribute(
                "style").strip() == ""
        )

    def wait_number_input_errors_visible(self):
        self.wait.until(
            lambda d: d.find_element(
                *PaymentCardFormLocators.error_number_input).get_attribute(
                "style").strip() == ""
        )
        self.wait.until(
            lambda d: d.find_element(
                *PaymentCardFormLocators.error_number_input_text).get_attribute(
                "style").strip() == ""
        )

    def scroll_to_premium_form(
            self):  # скролл для формы, которая не убирается в открытом браузере и обрезается (можно переиспользовать для других длинных форм)
        form = self.find_element_visible(PremiumBuyFormLocators.main_form)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'start', inline: 'nearest'});",
            form)

    def should_show_price(self):
        return self.find_element_visible(PremiumBuyFormLocators.price)

    def go_to_payment_page(self):
        self.click(PremiumBuyFormLocators.submit_button)

    def should_be_premium_card_form_page(self):
        self.find_element_visible(PaymentCardFormLocators.card_form_title)

    def fill_card_number_with_js(self, card_number=CARD_NUMBER):
        if card_number is not None:
            card_number_input = self.find_clickable(
                PaymentCardFormLocators.card_number_input)
            # обход ошибки при вводе номера карты через send_keys() - вставка номера в поле сразу целиком через JavaScript
            self.driver.execute_script("arguments[0].value = arguments[1];",
                                       card_number_input, card_number)
            self.click(PaymentCardFormLocators.card_number_input)

    def fill_card_number(self, card_number=CARD_NUMBER):
        if card_number is not None:
            self.type(PaymentCardFormLocators.card_number_input, card_number)

    def fill_card_date(self, card_date=CARD_DATE):
        if card_date is not None:
            self.click(PaymentCardFormLocators.card_date_input)
            self.type(PaymentCardFormLocators.card_date_input, card_date)

    def should_hide_card_date_errors(self):
        # ждем исчезновения ошибки, которая скорее всего возникает из-за предыдущей махинации с JavaScript (больше не смогла ничего придумать)
        self.element_invisible(PaymentCardFormLocators.error_date_input_text)

    def fill_card_csv(self, card_vscode=CARD_CSV):
        if card_vscode is not None:
            self.type(PaymentCardFormLocators.card_csv_input, card_vscode)

    def fill_card_name(self, card_name=CARD_NAME):
        if card_name is not None:
            self.type(PaymentCardFormLocators.card_name_input, card_name)

    def fill_card_form(self, card_number=CARD_NUMBER, card_date=CARD_DATE,
                       card_csv=CARD_CSV, card_name=CARD_NAME):
        if card_number is not None:
            self.fill_card_number_with_js(card_number)
        if card_date is not None:
            self.fill_card_date(card_date)
        if card_csv is not None:
            self.fill_card_csv(card_csv)
        if card_name is not None:
            self.fill_card_name(card_name)

    # JS код который убирает фокус из инпутов (обводку) - для скриншот-тестов
    def blur_active_elements(self):
        self.driver.execute_script("document.activeElement.blur();")

    def should_submit_button_be_active(self):
        self.element_invisible(PaymentCardFormLocators.submit_button_disabled)

    def go_to_3ds_page(self):
        self.find_clickable(PaymentCardFormLocators.submit_button)
        self.click(PaymentCardFormLocators.submit_button)

    def should_be_3ds_page(self):
        self.find_element_visible(ConfirmationPaymentFormLocators.title)

    def fill_secure_code(self, secure_code=SECURE_CODE):
        self.type(ConfirmationPaymentFormLocators.code_input, secure_code)

    def confirm_payment(self):
        self.click(ConfirmationPaymentFormLocators.submit_button_3ds)

    def should_show_premium_status(self):
        return self.find_element_visible(PaymentSuccessLocators.payment_status)

    def back_to_store(self):
        self.click(PaymentSuccessLocators.back)

    def should_show_success_premium(self):
        self.find_element_visible(PremiumSuccessLocators.title_premium)

    def back_to_main(self):
        self.click(PremiumSuccessLocators.submit_button_ok)

    def should_show_invalid_card_number_errors(self):
        self.find_element_visible(PaymentCardFormLocators.error_number_input)
        self.find_element_visible(
            PaymentCardFormLocators.error_number_input_text)

    def should_show_invalid_card_date_errors(self):
        self.find_element_visible(PaymentCardFormLocators.error_date_input)
        self.find_element_visible(
            PaymentCardFormLocators.error_date_input_text)

    def should_show_disabled_submit_button(self):
        self.find_element_visible(
            PaymentCardFormLocators.submit_button_disabled)

    def cancel_premium(self):
        self.click(CancelPremiumLocators.cancel_premium_button)

    def confirm_cancellation(self):
        self.click(CancelPremiumLocators.cancel_go_premium_button)

    def should_show_success_cancellation(self):
        self.find_element_visible(CancelPremiumLocators.pre_title)

    def back_to_trainer_page_after_cancellation(self):
        self.click(CancelPremiumLocators.back_button)
