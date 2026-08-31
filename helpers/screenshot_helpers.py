class InvalidLocatorError(Exception):
    pass


def hide_element(driver, locator):
    # проверяем, есть ли у объекта метод get_attribute
    if hasattr(locator, "get_attribute"):
        elements = [locator]
    elif isinstance(locator, tuple):
        elements = driver.find_elements(*locator)
    else:
        raise InvalidLocatorError("Некорректный элемент/локатор")
    for el in elements:
        # выполняем JS скрипт для скрытия: 1) убираем анимацию если есть 2)делаем элемент полностью прозрачным
        driver.execute_script(
            "arguments[0].style.transition='none';"
            "arguments[0].style.opacity='0';", el
        )
