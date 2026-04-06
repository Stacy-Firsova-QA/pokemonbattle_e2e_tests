import pytest
import os
import allure
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.pokemons_list_locators import PokemonListLocators
from locators.trainer_page_locators import TrainerPageLocators
from locators.payment_forms_locators import PaymentSuccessLocators, PremiumSuccessLocators, PaymentCardFormLocators, PremiumBuyFormLocators, CancelPremiumLocators, ConfirmationPaymentFormLocators
from data.test_trainer_data import TEST_TRAINER_ID
from data.payment_data import CARD_CSV, CARD_DATE, CARD_NAME, CARD_NUMBER, SECURE_CODE
from helpers.premium_helpers import check_premium_status, slow_type

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

    @allure.title("Покупка премиума: успешный сценарий")
    def test_buy_premium_successfully(self, prepare_for_buy_premium, open_premium_page, api_session):
        wait = WebDriverWait(open_premium_page, 2)

        with allure.step("Ждем появления инпута для дней и вводим в него количество дней"):
            days_input = wait.until(EC.visibility_of_element_located(PremiumBuyFormLocators.days_input))
            days_input.send_keys("2")

        with allure.step("Ждем появления расчитанной суммы и проверяем ее значение"):
            price = wait.until(EC.visibility_of_element_located(PremiumBuyFormLocators.price))
            assert "200" in price.text, "Сумма не соответствует ожидаемой"

        with allure.step("Ждем появления кнопки 'Перейти к оплате' и кликаем на нее"):
            submit_button = wait.until(EC.element_to_be_clickable(PremiumBuyFormLocators.submit_button))
            submit_button.click()

        with allure.step("Ждем появления расчитанной суммы и проверяем ее значение на экране оплаты"):
            payment_number = wait.until(EC.visibility_of_element_located(PaymentCardFormLocators.payment_number))
            assert "200" in payment_number.text, "Передалась неверная сумма"

        with allure.step("Ожидаем поле ввода номера карты и вводим номер карты"):
            card_number_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_number_input))
            # здесь пришлось прибегнуть к вспомогательной функции в которой применяется time.sleep(), так как обычный ввод номера выдавал ошибку валидации поля
            slow_type(card_number_input, CARD_NUMBER)

        with allure.step("Ожидаем поле ввода срока карты и вводим дату"):
            card_date_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_date_input))
            card_date_input.send_keys(CARD_DATE)

        with allure.step("Ожидаем поле ввода csv карты вводим его"):
            card_csv_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_csv_input))
            card_csv_input.send_keys(CARD_CSV)

        with allure.step("Ожидаем поле ввода имя карты и вводим его"):
            card_name_input = wait.until(EC.element_to_be_clickable(PaymentCardFormLocators.card_name_input))
            card_name_input.send_keys(CARD_NAME)
            card_name_input.click()

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
            wait.until(EC.visibility_of_element_located(PaymentSuccessLocators.payment_status))

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

