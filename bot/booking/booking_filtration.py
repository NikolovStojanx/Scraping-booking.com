from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        start_filtration_box = self.driver.find_element(By.XPATH, '//div[@data-filters-group="class"]')
        star_child_elements = start_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        for star_value in star_values:

            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    wait = WebDriverWait(self.driver, 5)
                    wait.until(EC.element_to_be_clickable(star_element))
                    star_element.click()


    def sort_price_lowest_first(self):
        pass
