import os
import time
from http import HTTPStatus


def check_premium_status(api_session):
    response_me = api_session.get(
        os.getenv("POKEMONBATTLE_HOST") + "/me",
    )
    assert response_me.status_code == HTTPStatus.OK
    body_me = response_me.json()["data"][0]
    return body_me["is_premium"]

def cancel_premium(api_session):
    res = api_session.post(
        os.getenv("LAVKA_HOST") + "/cancel_premium"
    )
    assert res.status_code == HTTPStatus.OK
    body = res.json()
    assert body["message"] == "Пользователь потерял премиум"

def buy_premium(api_session):
    response_buy = api_session.post(
        os.getenv("LAVKA_HOST") + "/payments",
        json={
            "order_type": "premium",
            "details": {
                "days": 12,
                "card_number": "4111111111111111",
                "card_name": "test testov",
                "card_actual": "10/28",
                "card_cvv": "125",
                "secure_code": "56456"
            }
        }
    )
    assert response_buy.status_code == HTTPStatus.OK
    body = response_buy.json()
    assert body["message"] == "Транзакция успешна"
    assert body["days"] == 12

# здесь через delay задаем паузу между вводимыми символами, которая будет применяться в time.sleep()
def slow_type(element, text, delay=0.1):
    element.click()
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(delay)