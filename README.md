# PokemonBattle E2E Tests

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)](https://docs.pytest.org/)
[![Selenium](https://img.shields.io/badge/UI-Selenium-43B02A.svg?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Allure Report](https://img.shields.io/badge/reports-Allure-orange.svg)](https://allurereport.org/)
[![CI](https://github.com/Stacy-Firsova-QA/pokemonbattle_e2e_tests/actions/workflows/ci.yml/badge.svg)](https://github.com/Stacy-Firsova-QA/pokemonbattle_e2e_tests/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

UI end-to-end test suite for [PokemonBattle](https://pokemonbattle.ru), a public training web app used to practice test automation. Built with the Page Object pattern on top of Selenium, plus a small visual-regression layer for pixel-level UI checks. This project is the UI counterpart to [pokemonbattle_api_tests](https://github.com/Stacy-Firsova-QA/pokemonbattle_api_tests) — API preparation/cleanup and UI verification are combined in the same tests where it makes sense (e.g. buying a Premium subscription through the UI, then confirming the result via the API).

## What's covered

| Area | Scenario |
|---|---|
| Login | Authorize with a real account and land on the trainer's page |
| Navigation | Go from the pokemons list to the trainer page |
| Trainer page | The "beginning" achievement icon is active for a fresh trainer |
| Trainer page | Navigate from the trainer page to the Premium purchase form |
| Premium purchase | Buy Premium with different CVV values — success and two negative/error scenarios |
| Premium purchase | Premium price calculation matches the pricing table for a range of day counts |
| Premium purchase | Invalid card number / invalid card date are rejected with the right on-screen error |
| Premium cancellation | Cancel an active Premium subscription and verify the confirmation screen |
| Visual regression | Screenshot comparisons for the trainer page and the Premium purchase forms |

## Test architecture

- **Page Object pattern** (`pages/`) — `BasePage` provides shared waits/clicks/typing helpers with readable failure messages; each page (`LoginPage`, `TrainerPage`, `PokemonsPage`, `PremiumPages`) exposes actions and assertions in terms of the UI, not raw Selenium calls.
- **`locators/`** — element locators grouped by page, kept separate from page logic.
- **`fixtures/ui_fixtures.py`** — builds the Selenium driver and chains together the "already logged in" → "on the trainer page" → "on the premium form" setup steps as composable fixtures.
- **`fixtures/api_fixtures.py`** + **`helpers/premium_helpers.py`** — a lightweight API client used to prepare and verify backend state around UI actions (e.g. making sure Premium is off before a "buy" test, or double-checking Premium actually got cancelled), including a poll-until-consistent helper for cases where the UI and backend can briefly disagree.
- **`tests/screenshot/`** — visual regression tests (via `pytest-playwright-snapshot`) with baseline images committed under `tests/screenshot/__snapshots__/`, plus custom diff-highlighting logic in `conftest.py` for quick visual debugging of a failure.

## Tech stack

- **Python 3.12**, **pytest 9**
- **selenium** + **webdriver-manager** — browser automation
- **playwright** / **pytest-playwright-snapshot** — screenshot/visual regression testing
- **Pillow**, **pixelmatch** — image diffing for failed screenshot comparisons
- **allure-pytest** — reporting
- **python-dotenv** — configuration via `.env`

## Project structure

```
pokemonbattle_e2e_tests/
├── data/                             # test data and constants
│   ├── payment_data.py
│   └── test_trainer_data.py
├── fixtures/
│   ├── api_fixtures.py               # API-side setup/teardown for UI tests
│   └── ui_fixtures.py                # driver + page-chain fixtures
├── helpers/
│   ├── premium_helpers.py            # API calls + pricing logic used across tests
│   └── screenshot_helpers.py         # element masking for screenshot tests
├── locators/                         # Selenium locators, one file per page
├── pages/                            # Page Object classes
├── tests/
│   ├── e2e/                          # functional UI scenarios
│   └── screenshot/                   # visual regression tests
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Quick start

```bash
git clone https://github.com/Stacy-Firsova-QA/pokemonbattle_e2e_tests.git
cd pokemonbattle_e2e_tests

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium     # only needed for the screenshot tests

cp .env.example .env            # fill in LOGIN, PASSWORD, hosts and a trainer token
```

Run the functional e2e tests with an Allure report:

```bash
pytest tests/e2e -v --alluredir=allure-results
allure serve allure-results
```

Run the visual regression tests:

```bash
pytest tests/screenshot -v
```

## CI

On every push and pull request to `main`, GitHub Actions (`.github/workflows/ci.yml`) lints the code with [ruff](https://docs.astral.sh/ruff/) and runs the **functional tests in `tests/e2e/`** against the live site, using credentials and hosts stored as repository secrets. The Selenium driver isn't configured for headless mode (so a local run pops up a real browser window), so CI runs it under a virtual X display ([Xvfb](https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml)) instead of modifying that behavior.

The visual regression tests in `tests/screenshot/` are intentionally **not** run in CI: their baseline images were captured on macOS, and font/anti-aliasing differences on a Linux CI runner would produce false failures on every run regardless of whether the UI actually changed. They're meant to be run locally, on the same OS the baselines were generated on (or after regenerating baselines for the CI environment, which this project doesn't currently do).

## Author

**Anastasia Firsova** — QA Automation Engineer.
GitHub: [Stacy-Firsova-QA](https://github.com/Stacy-Firsova-QA)

## License

This project is licensed under the [MIT License](LICENSE).
