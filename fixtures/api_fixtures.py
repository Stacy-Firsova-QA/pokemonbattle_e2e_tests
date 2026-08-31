import os

import allure
import pytest
import requests

from helpers.premium_helpers import (
    buy_premium,
    cancel_premium,
    check_premium_status,
    wait_premium_status,
)


# сделала одну сессию на все запросы, так как запросов апи будет пока немного и расширять логику пока нет смысла
@pytest.fixture(scope="session")
def api_session():
    with allure.step("Создание API сессии"), requests.Session() as main_session:
        main_session.headers.update(
            {"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
        yield main_session


@pytest.fixture()
def prepare_for_buy_premium(api_session):
    if check_premium_status(api_session):
        cancel_premium(api_session)
        wait_premium_status(api_session, False)

    assert check_premium_status(api_session) is False

    yield

    if check_premium_status(api_session):
        cancel_premium(api_session)
        wait_premium_status(api_session, False)


@pytest.fixture()
def prepare_for_cancel_premium(api_session):
    if check_premium_status(api_session) is False:
        buy_premium(api_session)
        wait_premium_status(api_session, True)

    assert check_premium_status(api_session) is True

    yield

    if check_premium_status(api_session):
        cancel_premium(api_session)
        wait_premium_status(api_session, False)
