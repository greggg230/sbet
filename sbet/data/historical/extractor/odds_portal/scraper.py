import csv
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, auto
from time import sleep
from typing import Any, List, Optional

from requests import get, JSONDecodeError
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from sbet.data.historical.extractor.odds_portal.parse import parse_odds_portal_json

fragments_by_year = {
    2024: "4zIGLOIo",
    2023: "AZ3pnDvF",
    2022: "SIrupo05",
    2021: "pALSpRpa",
    2020: "vsI7DL6R",
    2019: "002DshSN",
    2018: "KM2qHMND",
    2017: "hIani0sm",
    2016: "WvRyBSTq",
    2015: "Whx6oNSf",
    2014: "SOcxLnmF",
    2013: "lhwryinh",
    2012: "OjGY6aVA",
    2011: "02jHmMIF",
    2010: "KUzfp5N3",
    2009: "C0yUqo8c",
    2008: "Y9xQpRhi",
    2007: "Cr5OImBN",
    2006: "Yi6KJTeH",
    2005: "Eof1J9tB",
    2004: "4ULH6kR4",
    2003: "A7MD7VBb",
    2002: "d4I98Bdh",
    2001: "EuT49isn",
    2000: "zkU0AXRu",
    1999: "t4UQmldU",
    1998: "2DVMlUtO"
}

# Base URL format
url_template = "https://www.oddsportal.com/ajax-sport-country-tournament-archive_/1/{}/X220577832X9003016X65536X0X136839680X57472X0X0X0X0X4194304X0X4096X673251333X512X1179650X0X0X1024X18464X131072X256X0X0X0X0X131072/1/0/"

# Generate URLs
urls = {year: url_template.format(fragment) for year, fragment in fragments_by_year.items()}


class SoccerOutcome(Enum):
    HOME_WIN = auto()
    AWAY_WIN = auto()
    DRAW = auto()


@dataclass(frozen=True)
class BetEntry:
    game_date: date
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    home_win_price: float
    draw_price: float
    away_win_price: float
    outcome: SoccerOutcome


def parse_row(element: WebElement, game_date: date) -> Optional[BetEntry]:
    home_team = element.find_element(By.XPATH, "./a[1]/div[1]/div[2]/div[1]/div[1]/a[1]").text
    away_team = element.find_element(By.XPATH, "./a[1]/div[1]/div[2]/div[1]/div[1]/a[2]").text

    try:
        home_score = int(element.find_element(By.XPATH, "./a[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]").text)
        away_score = int(element.find_element(By.XPATH, "./a[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]").text)
    except NoSuchElementException:
        return None

    home_win_price_el = element.find_element(By.XPATH, "./div[1]")
    draw_price_el = element.find_element(By.XPATH, "./div[2]")
    away_win_price_el = element.find_element(By.XPATH, "./div[3]")

    def check_if_outcome_happened(outcome_element: WebElement) -> bool:
        return "gradient-green" in outcome_element.find_element(By.XPATH, "./div[1]/div[1]/p[1]").get_attribute("class").split(" ")

    try:
        home_win_price = float(home_win_price_el.text.replace("\nAdd to my coupon", ""))
        away_win_price = float(away_win_price_el.text.replace("\nAdd to my coupon", ""))
        draw_price = float(draw_price_el.text.replace("\nAdd to my coupon", ""))
    except ValueError:
        return None

    outcome: SoccerOutcome
    if check_if_outcome_happened(home_win_price_el):
        outcome = SoccerOutcome.HOME_WIN
    elif check_if_outcome_happened(draw_price_el):
        outcome = SoccerOutcome.DRAW
    elif check_if_outcome_happened(away_win_price_el):
        outcome = SoccerOutcome.AWAY_WIN
    else:
        raise Exception("Could not identify outcome.")

    return BetEntry(
        game_date=game_date,
        home_team=home_team,
        away_team=away_team,
        home_score=home_score,
        away_score=away_score,
        home_win_price=home_win_price,
        away_win_price=away_win_price,
        draw_price=draw_price,
        outcome=outcome
    )


def parse_year_page(browser: WebDriver) -> List[BetEntry]:
    browser.find_elements()

    bet_entries: List[BetEntry] = []

    elements = browser.find_elements(By.XPATH, f"//div[contains(@class, 'eventRow')]")
    current_date: Optional[date] = None

    def parse_date(date_element: WebElement) -> date:
        scrub_strings = (" - Play Offs", " - All Stars", " - Qualification")

        scrubbed_string = date_element.text

        for s in scrub_strings:
            scrubbed_string = scrubbed_string.replace(s, "")

        return datetime.strptime(scrubbed_string, "%d %b %Y").date()

    for element in elements:
        game_index: int
        if len(element.find_elements(By.XPATH, './div')) == 3:
            current_date = parse_date(element.find_element(By.XPATH, './div[2]/div[1]'))
            game_index = 3
        elif len(element.find_elements(By.XPATH, './div')) == 2:
            current_date = parse_date(element.find_element(By.XPATH, './div[1]/div[1]'))
            game_index = 2
        else:
            game_index = 1

        game_element = element.find_element(By.XPATH, f"./div[{game_index}]/div[1]")
        parsed_row = parse_row(game_element, current_date)
        if parsed_row is not None:
            bet_entries.append(parsed_row)
    return bet_entries


def scrape_mls_odds() -> None:
    years = range(2024, 1997, -1)

    browser = webdriver.WebDriver()

    browser.get("https://www.oddsportal.com/football/usa/mls/results/")

    results:  List[BetEntry] = []

    for year in years:
        print(year)
        browser.execute_script("window.scrollTo(0, 0)")
        sleep(1)
        browser.find_element(By.XPATH, f"//a[text()=' {year} ']").click()
        sleep(2)
        browser.execute_script("window.scrollTo(0, 2160)")
        sleep(1)
        results.extend(parse_year_page(browser))
        while len(browser.find_elements(By.XPATH, "//a[text()='Next']")) != 0:
            print(".")
            next_link = browser.find_element(By.XPATH, "//a[text()='Next']")
            next_link.click()
            sleep(4)
            browser.execute_script("window.scrollTo(0, 2160)")
            sleep(1)
            results.extend(parse_year_page(browser))

    with open('mls.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'home', 'away', 'home_score', 'away_score', 'home_win_price', 'away_win_price', 'draw_price', 'outcome'])
        for result in results:
            writer.writerow([
                result.game_date.strftime("%Y-%m-%d"),
                result.home_team,
                result.away_team,
                result.home_score,
                result.away_score,
                result.home_win_price,
                result.away_win_price,
                result.draw_price,
                result.outcome.value
            ])


if __name__ == "__main__":
    scrape_mls_odds()


