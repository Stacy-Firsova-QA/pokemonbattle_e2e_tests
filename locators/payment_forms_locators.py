from selenium.webdriver.common.by import By

class PremiumBuyFormLocators:

    profile_title = (By.XPATH, "//div[contains(@class, 'k_page_main_premium')]/div[@class='profile-mobile-wrapper']/h1")
    days_input = (By.CLASS_NAME, "k_input_days")
    price = (By.CSS_SELECTOR, "div.k_price_premium > span")
    submit_button = (By.ID, "buy-premium")

class PaymentCardFormLocators:

    payment_number = (By.XPATH, "//div[@class='payment_receipt_open_button']/p[contains(text(), '200')]")
    card_number_input = (By.CLASS_NAME, "card_number")
    card_date_input = (By.CLASS_NAME, "card_date")
    card_csv_input = (By.CLASS_NAME, "card_csv")
    card_name_input = (By.CLASS_NAME, "card_name")
    submit_button = (By.XPATH, "//button[text()='Оплатить']")

class ConfirmationPaymentFormLocators:

    title = (By.XPATH, "//h3[text()='Подтверждение покупки']")
    code_input = (By.CLASS_NAME, "threeds_number")
    submit_button_3ds = (By.XPATH, "//button[text()='Оплатить']")

class PaymentSuccessLocators:

    payment_status = (By.XPATH, "//h3[text()='Покупка прошла успешно']")
    back = (By.XPATH, "//p[text()='Вернуться в магазин']")

class PremiumSuccessLocators:

    title_premium = (By.XPATH, "//div[@class='k_title_premium' and text()='Премиум успешно подключен!']")
    submit_button_ok = (By.ID, "ok-battles-premium")

class CancelPremiumLocators:

    cancel_premium_button = (By.ID, "cancel-premium")
    # локаторы в следующем окне после нажатия на кнопку "отменить подписку"
    cancel_go_premium_button = (By.ID, "cancel-go-premium")
    # локаторы в следующем окне после подтверждения отмены премиума
    pre_title = (By.XPATH, "//div[text()='Вы отменили подписку :(']")
    back_button = (By.CLASS_NAME, "top_back_button_text")
