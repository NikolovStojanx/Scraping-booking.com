from selenium import webdriver
import time
import bot.booking.constants as const
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bot.booking.booking_filtration import BookingFiltration
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettytable import PrettyTable

from bot.booking.booking_report import BookingReport


class Booking(webdriver.Chrome):

    def __init__(self, driver_path='E:/ChromeDriver/chromedriver-win64/chromedriver.exe', teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += os.pathsep + driver_path
        options = Options()
        # options.add_experimental_option("detach", True)
        # options.add_argument('--headless')  # <-- Headless mode
        # options.add_argument('--disable-gpu')  # <-- Optional, for Windows
        # options.add_argument('--window-size=1920,1080')  # Recommended for full-page rendering
        # options.add_argument('--no-sandbox')  # Optional, helps in some environments
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(1)
        self.maximize_window()


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_menu = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_menu.click()

        currency_button = self.find_element(By.XPATH, f"//div[contains(text(), '{currency}')]/ancestor::button")
        currency_button.click()


    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.XPATH, '//input[@name="ss"]')
        # search_field.clear()
        time.sleep(0.5)
        search_field.send_keys(place_to_go)
        wait = WebDriverWait(self, 3.5)
        autocomplete_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//li[@id="autocomplete-result-0"]'))
        )
        autocomplete_option.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.XPATH, f'//table/tbody//tr//td/span[@data-date="{check_in_date}"]')
        check_in_element.click()
        check_out_element = self.find_element(By.XPATH, f'//table/tbody//tr//td/span[@data-date="{check_out_date}"]')
        check_out_element.click()
        time.sleep(1)

    def select_adults(self, count):
        selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection_element.click()
        div_container = selection_element.find_element(By.XPATH, 'ancestor::div')
        [decrease_button, increase_button] = div_container.find_elements(By.XPATH, '//label[text()="Adults"]/parent::div/parent::div/div[2]/button')

        count_of_adults = int(decrease_button.find_element(By.XPATH, '//label[text()="Adults"]/parent::div/parent::div/div[2]/span').text.strip())

        while count_of_adults >= 2:
            count_of_adults -= 1
            decrease_button.click()


        for _ in range(count - 1):
            increase_button.click()


    def click_search(self):
        submit_button = self.find_element(By.XPATH,
                                          '//button[@type="submit"]'
                                            )
        submit_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3)
    # <div class="d4924c9e74" role="list" data-results-container="1">
    def report_results(self):
        hotel_boxes = self.find_element(By.XPATH, '//div[@data-results-container="1"]')
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names = ["Hotel Name", "Hotel Price", "Hotel Score", "Hotel Location Score"]
        )
        table.add_rows(report.pull_deal_box_info())
        print(table)
