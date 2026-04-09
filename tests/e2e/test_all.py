import pytest
import os
import allure
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.pokemons_list_locators import PokemonListLocators
from locators.trainer_page_locators import TrainerPageLocators
from locators.payment_forms_locators import PaymentSuccessLocators, PremiumSuccessLocators, PaymentCardFormLocators, PremiumBuyFormLocators, CancelPremiumLocators, ConfirmationPaymentFormLocators
from data.test_trainer_data import TEST_TRAINER_ID
from data.payment_data import CARD_CSV, CARD_DATE, CARD_NAME, CARD_NUMBER, SECURE_CODE
from helpers.premium_helpers import check_premium_status, calculate_premium_price

@allure.suite("Тесты авторизации")
class TestAuthorization:

    @allure.title("Авторизация: успешный сценарий")
    def test_authorization_successfully(self, driver, authorization):
        # оставила здесь такой вариант ожидания в учебных целях
        driver.implicitly_wait(2)

        trainer_card = driver.find_element(*PokemonListLocators.trainer_card_id)
        with allure.step("Проверяем, что видим превью карточки тренера на главной"):
            assert trainer_card.is_displayed()
        with allure.step("Проверяем, что отображается урл для главной"):
            assert driver.current_url == os.getenv("BASE_URL") + "/"

@allure.suite("Тесты на переходы")
class TestRedirects:

    @allure.title("Переход с главной страницы на страницу тренера")
    def test_from_main_to_trainer_page(self, driver, authorization):
        wait = WebDriverWait(driver, 2)

        trainer_card = wait.until(EC.element_to_be_clickable(PokemonListLocators.trainer_card_id))
        trainer_card.click()

        wait.until(EC.visibility_of_element_located(TrainerPageLocators.trainer_name))
        with allure.step("Проверяем, что отображается урл для экрана тренера"):
            assert driver.current_url == f"{os.getenv('BASE_URL')}/trainer/{TEST_TRAINER_ID}"

    @allure.title("Тест на переход со страницы тренера на страницу оформления премиума")
    def test_from_trainer_page_to_premium(self, open_trainer_page):
        wait = WebDriverWait(open_trainer_page, 2)

        with allure.step("Ожидаем доступность таба Премиум для перехода и кликаем по нему"):
            premium_tab = wait.until(EC.element_to_be_clickable(TrainerPageLocators.to_premium))
            premium_tab.click()

        with allure.step("Ожидаем отображения названия формы для покупки премиума"):
            wait.until(EC.visibility_of_element_located(PremiumBuyFormLocators.profile_title))
        with allure.step("Проверяем, что отображается урл для покупки премиума"):
            assert open_trainer_page.current_url == os.getenv("BASE_URL") + "/premium"

@allure.suite("Проверки элементов на странице тренера")
class TestElementsOnTrainerPage:

    @allure.title("Проверка активной ачивки 'Начало большого пути' на странице тренера")
    def test_check_achiev_beginning_icon_active(self, open_trainer_page):
        wait = WebDriverWait(open_trainer_page, 2)

        with allure.step("Ждем появления иконки ачивки и проверяем, что оно отображается"):
            wait.until(EC.visibility_of_element_located(TrainerPageLocators.beginning_icon_active))

@allure.suite("Тесты на покупку премиума")
class TestBuyPremium:

    @allure.title("Покупка премиума: разные сценарии оплаты через csv")
    @pytest.mark.parametrize("card_csv, expected_result, expected_text", [
        ("125", "success", "Покупка прошла успешно"),
        ("126", "error", "При оплате произошла ошибка"),
        ("300", "error", "При оплате произошла ошибка"),
    ], ids=["success result", "error result: insufficient funds", "error result: invalid csv"])
    def test_buy_premium_different_csv_values(self, prepare_for_buy_premium, open_premium_page, api_session, card_csv, expected_result, expected_text):
        wait = WebDriverWait(open_premium_page, 4)

        with allure.step("Ждем появления инпута для дней и вводим в него количество дней"):
            days_input = wait.until(EC.visibility_of_element_located(PremiumBuyFormLocators.days_input))
            days_input.send_keys("2")

        with allure.step("Ждем появления кнопки 'Перейти к оплате' и кликаем на нее"):
            submit_button = wait.until(EC.element_to_be_clickable(PremiumBuyFormLocators.submit_button))
            submit_button.click()

        with allure.step("Ожидаем поле ввода номера карты и вводим номер карты"):
            card_number_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_number_input))
            # обход ошибки при вводе номера карты через send_keys() - вставка номера в поле сразу целиком через JavaScript
            open_premium_page.execute_script("arguments[0].value = arguments[1];", card_number_input, CARD_NUMBER)

        with allure.step("Ожидаем поле ввода срока карты и вводим дату"):
            card_date_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_date_input))
            card_date_input.send_keys(CARD_DATE)
            # ждем исчезновения ошибки, которая скорее всего возникает из-за предыдущей махинации с JavaScript (больше не смогла ничего придумать)
            wait.until(EC.invisibility_of_element_located(PaymentCardFormLocators.error_date_input_text))

        with allure.step("Ожидаем поле ввода csv карты вводим его"):
            card_csv_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_csv_input))
            card_csv_input.send_keys(card_csv)

        with allure.step("Ожидаем поле ввода имя карты и вводим его"):
            card_name_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_name_input))
            card_name_input.send_keys(CARD_NAME)

        with allure.step("Ожидаем кнопку оплаты и кликаем по ней"):
            submit_payment_button = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.submit_button))
            submit_payment_button.click()

        with allure.step("Проверяем, что перешли на окно потверждения оплаты"):
            wait.until(EC.visibility_of_element_located(ConfirmationPaymentFormLocators.title))

        with allure.step("Ожидаем поле ввода кода и вводим его"):
            secure_code = wait.until(EC.element_to_be_clickable(ConfirmationPaymentFormLocators.code_input))
            secure_code.send_keys(SECURE_CODE)

        with allure.step("Ожидаем кнопку оплаты и кликаем по ней"):
            submit_payment3ds_button = wait.until(EC.element_to_be_clickable(ConfirmationPaymentFormLocators.submit_button_3ds))
            submit_payment3ds_button.click()

        with allure.step("Проверяем статус покупки"):
            status = wait.until(EC.visibility_of_element_located(PaymentSuccessLocators.payment_status))

        if expected_result == "success":
            with allure.step("Проверяем успешный статус текста"):
                assert expected_text in status.text

            with allure.step("Возвращаемся в магазин"):
                button_back = wait.until(EC.element_to_be_clickable(PaymentSuccessLocators.back))
                button_back.click()

            with allure.step("Проверяем уведомление об успешном подключении премиума и переходим с него на главную"):
                wait.until(EC.visibility_of_element_located(PremiumSuccessLocators.title_premium))
                submit_premium_button = wait.until(EC.element_to_be_clickable(PremiumSuccessLocators.submit_button_ok))
                submit_premium_button.click()

            with allure.step("Проверяем, что оказались на главной"):
                assert open_premium_page.current_url == os.getenv("BASE_URL") + "/"

            with allure.step("Проверяем, что подписка действительно подключилась через запрос"):
                assert check_premium_status(api_session) is True

        else:
            with allure.step("Проверяем неуспешный статус текста"):
                assert expected_text in status.text

            with allure.step("Возвращаемся в магазин"):
                button_back = wait.until(EC.element_to_be_clickable(PaymentSuccessLocators.back))
                button_back.click()

            with allure.step("Проверяем, что подписка не подключилась через запрос"):
                assert check_premium_status(api_session) is False

    @allure.title("Проверка расчета стоимости Премиума: успешный сценарий")
    def test_calculate_premium_price(self, prepare_for_buy_premium, open_premium_page):
        wait = WebDriverWait(open_premium_page, 2)

        days = (random.randint(1, 999))
        expected_price = calculate_premium_price(days)
        # как работает:
        # ":" - значит "дальше идут правила форматирования"
        # "," - значит "разделяй тысячи"
        expected_price_formatted = f"{expected_price:,}".replace(",", " ")

        with allure.step("Ждем появления инпута для дней и вводим в него количество дней"):
            days_input = wait.until(EC.visibility_of_element_located(PremiumBuyFormLocators.days_input))
            days_input.send_keys(str(days))

        with allure.step("Ждем появления рассчитанной суммы и проверяем ее значение"):
            price_premium = wait.until(EC.visibility_of_element_located(PremiumBuyFormLocators.price))
            assert expected_price_formatted in price_premium.text, "Сумма не соответствует ожидаемой"

    @allure.title("Ввод невалидного номера карты для оплаты: негативный сценарий")
    def test_invalid_card_number(self, prepare_for_buy_premium, open_premium_card_form_page, api_session):
        wait = WebDriverWait(open_premium_card_form_page, 2)

        with allure.step("Ожидаем поле ввода номера карты и вводим номер карты"):
            card_number_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_number_input))
            # обход ошибки при вводе номера карты через send_keys() - вставка номера в поле сразу целиком через JavaScript
            open_premium_card_form_page.execute_script("arguments[0].value = arguments[1];", card_number_input, "4111111111111112")
            card_number_input.click()

        with allure.step("Ожидаем поле ввода срока карты и вводим дату"):
            card_date_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_date_input))
            card_date_input.click()
            card_date_input.send_keys(CARD_DATE)
            wait.until(EC.invisibility_of_element_located(PaymentCardFormLocators.error_date_input_text))

        with allure.step("Ожидаем поле ввода csv карты вводим его"):
            card_csv_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_csv_input))
            card_csv_input.send_keys(CARD_CSV)

        with allure.step("Ожидаем поле ввода имя карты и вводим его"):
            card_name_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_name_input))
            card_name_input.send_keys(CARD_NAME)
            card_name_input.click()

        with allure.step("Ожидаем текст ошибки у поля и его подсветку"):
            wait.until(EC.visibility_of_element_located(PaymentCardFormLocators.error_input))
            wait.until(EC.visibility_of_element_located(PaymentCardFormLocators.error_input_text))

        with allure.step("Проверяем, что кнопка оплаты задизейблена"):
            wait.until(EC.visibility_of_element_located(PaymentCardFormLocators.submit_button_disabled))

    def test_invalid_card_date(self, prepare_for_buy_premium, open_premium_card_form_page, api_session):
        wait = WebDriverWait(open_premium_card_form_page, 2)

        with allure.step("Ожидаем поле ввода номера карты и вводим номер карты"):
            card_number_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_number_input))
            # обход ошибки при вводе номера карты через send_keys() - вставка номера в поле сразу целиком через JavaScript
            open_premium_card_form_page.execute_script("arguments[0].value = arguments[1];", card_number_input, CARD_NUMBER)

        with allure.step("Ожидаем поле ввода срока карты и вводим невалидную дату (в прошлом)"):
            card_date_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_date_input))
            card_date_input.send_keys("1020")

        with allure.step("Ожидаем текст ошибки у поля и его подсветку"):
            wait.until(EC.visibility_of_element_located(PaymentCardFormLocators.error_date_input))
            wait.until(EC.visibility_of_element_located(PaymentCardFormLocators.error_date_input_text))

        with allure.step("Ожидаем поле ввода csv карты вводим его"):
            card_csv_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_csv_input))
            card_csv_input.send_keys(CARD_CSV)

        with allure.step("Ожидаем поле ввода имя карты и вводим его"):
            card_name_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_name_input))
            card_name_input.send_keys(CARD_NAME)
            card_name_input.click()

        with allure.step("Проверяем, что кнопка оплаты задизейблена"):
            wait.until(EC.visibility_of_element_located(PaymentCardFormLocators.submit_button_disabled))

@allure.suite("Тесты на отмену премиума")
class TestCancelPremium:

    @allure.title("Отмена премиума: успешный сценарий")
    def test_cancel_premium_successfully(self, prepare_for_cancel_premium, open_trainer_page, api_session):
        wait = WebDriverWait(open_trainer_page, 2)

        with allure.step("Ожидаем кнопку перехода к премиуму и кликаем на нее"):
            premium_button = wait.until(EC.element_to_be_clickable(TrainerPageLocators.to_premium))
            premium_button.click()

        with allure.step("Ожидаем кнопку отмены премиума и кликаем на нее"):
            cancel_button = wait.until(EC.element_to_be_clickable(CancelPremiumLocators.cancel_premium_button))
            cancel_button.click()

        with allure.step("Ожидаем кнопку отмены в подтверждающем окне и кликаем на нее"):
            cancel_go_premium_button = wait.until(EC.element_to_be_clickable(CancelPremiumLocators.cancel_go_premium_button))
            cancel_go_premium_button.click()

        with allure.step("Ожидаем сообщение об отмене подписки и проверяем его"):
            wait.until(EC.visibility_of_element_located(CancelPremiumLocators.pre_title))

        with allure.step("Возвращаемся на страницу тренера с информационного окна"):
            back_button = wait.until(EC.element_to_be_clickable(CancelPremiumLocators.back_button))
            back_button.click()

        with allure.step("Проверяем, что перешли на страницу тренера"):
            assert open_trainer_page.current_url == f"{os.getenv('BASE_URL')}/trainer/{TEST_TRAINER_ID}"

        with allure.step("Проверяем, что подписка действительно отменилась через запрос"):
            assert check_premium_status(api_session) is False

