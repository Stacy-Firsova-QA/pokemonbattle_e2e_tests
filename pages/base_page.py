from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class PageUrlNotSetError(Exception):
    pass


class BasePage:
    URL = None

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    # нужно для того, чтобы url считывался когда нужен, а не сразу (чтобы избежать ситуации, когда урл не подхватился из env при импорте)
    # для каждой страницы метод будет переопределен, поэтому по сути именно метод из base_page не будет никогда использоваться
    def get_url(self):
        if not self.URL:
            raise PageUrlNotSetError("self.URL is not set")
        return self.URL

    def open_page(self):
        self.open(self.get_url())

    def find_element_visible(self, by_locator: tuple[str, str],
                             element_name="Элемент"):
        # by_locator - это tuple из (by, locator)
        try:
            return self.wait.until(
                EC.visibility_of_element_located(by_locator))
        except TimeoutException:
            raise AssertionError(
                f"{element_name} по локатору {by_locator} не появился за время ожидания")

    def find_clickable(self, by_locator: tuple[str, str],
                       element_name="Элемент"):
        try:
            return self.wait.until(EC.element_to_be_clickable(by_locator))
        except TimeoutException:
            raise AssertionError(
                f"{element_name} по локатору {by_locator} не стал кликабельным за время ожидания")
        except ElementNotInteractableException:
            raise AssertionError(
                f"{element_name} по локатору {by_locator} найден, но с ним нельзя взаимодействовать")

    def click(self, by_locator: tuple[str, str], element_name="Элемент"):
        elem = self.find_clickable(by_locator, element_name)
        elem.click()
        return elem

    def type(self, by_locator: tuple[str, str], text: str,
             element_name="Элемент"):
        elem = self.find_element_visible(by_locator, element_name)
        elem.clear()
        elem.send_keys(text)
        return elem

    def element_invisible(self, by_locator: tuple[str, str],
                          element_name="Элемент"):
        try:
            return self.wait.until(
                EC.invisibility_of_element_located(by_locator))
        except TimeoutException:
            raise AssertionError(
                f"{element_name} по локатору {by_locator} не исчез за время ожидания")

    def should_have_url(self, expected_url: str):
        current_url = self.driver.current_url.rstrip("/")
        expected_url = expected_url.rstrip("/")
        assert current_url == expected_url, f"Ожидался URL {expected_url}, но был {current_url}"
