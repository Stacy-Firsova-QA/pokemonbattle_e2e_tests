import sys, os, io, pytest
from PIL import Image, ImageChops
from pathlib import Path
from dotenv import load_dotenv
from helpers.screenshot_helpers import hide_element

pytest_plugins = ["fixtures.api_fixtures", "fixtures.ui_fixtures"]

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture
def screenshot_test(assert_snapshot, request, browser_name):
    def run(
            driver,
            name: str,
            element=None,
            threshold: float = 0.05,
            baseline_dir: str = Path(request.node.fspath).parent.resolve() / "__snapshots__" / browser_name / sys.platform,
            diff_dir: str = "__screenshot_diffs__",
            mask: list = None
    ):
        # маскируем динамические элементы (опционально)
        if mask:
            for loc in mask:
                try:
                    hide_element(driver, loc)
                except Exception:
                    pass

        # снимок страницы или узла
        if element is None:  # снимок всей страницы, если элемент не указан
            png = driver.get_screenshot_as_png()
        else:
            if isinstance(element, tuple): # поиск элемента, если указан локатор для него
                element = driver.find_element(*element)
            png = element.screenshot_as_png # работа с WebElement напрямую, если передаем уже найденный элемент

        try:
            assert_snapshot(png, name=name, threshold=threshold)
            return
        except (AssertionError, ValueError):
            # AssertionError для отличия скриншотов, ValueError для отличия размеров элементов
            if not os.path.isdir(diff_dir):
                os.mkdir(diff_dir)

            baseline_path = os.path.join(baseline_dir, name)

            if name.lower().endswith(".png"):
                name = name[:-4]

            actual_path = os.path.join(diff_dir, f"{name}_actual.png")
            base_copy = os.path.join(diff_dir, f"{name}_baseline.png")
            diff_path = os.path.join(diff_dir, f"{name}_diff.png")

            actual = Image.open(io.BytesIO(png)).convert("RGBA")
            baseline = Image.open(baseline_path).convert("RGBA")

            actual.save(actual_path)
            baseline.save(base_copy)

            if actual.size != baseline.size:
                w = min(actual.width, baseline.width)
                h = min(actual.height, baseline.height)
                actual = actual.crop((0, 0, w, h))
                baseline = baseline.crop((0, 0, w, h))

            # подсвечиваем различия красным цветом
            diff = ImageChops.difference(baseline, actual)
            mask_img = diff.convert("L").point(lambda v: 255 if v > 10 else 0, mode="1")
            red = Image.new("RGB", actual.size, (255, 0, 0))
            highlight = actual.convert("RGB").copy()
            highlight.paste(red, mask=mask_img)

            highlight.save(diff_path)
            pytest.fail(
                f"Snapshot mismatch for '{name}'. "
                f"See {actual_path}, {base_copy}, {diff_path}"
            )

    return run