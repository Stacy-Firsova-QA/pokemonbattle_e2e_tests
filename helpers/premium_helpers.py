import os
import time
from http import HTTPStatus


def check_premium_status(api_session) -> bool:
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


def calculate_premium_price(days: int) -> int:
    if days < 30:
        return days * 30
    elif 30 <= days < 180:
        return days * 95
    elif 180 <= days < 365:
        return days * 90
    else:
        return days * 85


# нужно чтобы точно проверять, что премиум отменился/активировался, чтобы потом ui статус премиума совпадал с реальностью (а то они могут расходится - подготовка через апи может сработать а ui еще быть в неактуальном состоянии)
def wait_premium_status(api_session, expected_status: bool, timeout: int = 10,
                        poll: float = 1.0):
    end_time = time.time() + timeout

    while time.time() < end_time:
        if check_premium_status(api_session) is expected_status:
            return
        time.sleep(poll)

    raise AssertionError(
        f"Статус premium не стал {expected_status} за {timeout} секунд")
