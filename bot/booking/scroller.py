import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scroller:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def scroll_to_bottom(self, scroll_pause_time=1, max_scrolls=10):
        """Scrolls the page down and waits for new content to load"""
        scroll_height = self.driver.execute_script("return document.body.scrollHeight")
        new_scroll_height = 0
        scrolls = 0

        while scrolls < max_scrolls:
            # Scroll down by a certain amount
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and check if it has changed
            new_scroll_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_scroll_height == scroll_height:
                break  # No more new content loaded, stop scrolling

            scroll_height = new_scroll_height
            scrolls += 1

        return self.driver

    def load_more(self):
        button = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                                           "//button/span[contains(text(), 'Load more')]"))
        )
        # button = self.driver.find_element(By.XPATH, "//button/span[contains(text(), 'Load more')]")
        button.click()


    def load_all_data(self):

        while True:
            self.scroll_to_bottom()
            time.sleep(0.75)
            try:
                self.load_more()
            except Exception:
                break

