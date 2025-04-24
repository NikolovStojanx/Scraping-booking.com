from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot.booking import booking


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        ## //div[@data-testid="property-card"]
        deal_boxes = self.boxes_section_element.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")

        return deal_boxes

    def pull_deal_box_info(self):
        collection = []
        location_score = False
        for deal_box in self.deal_boxes:
            hotel_name = (deal_box.find_element(By.CSS_SELECTOR, "div[data-testid='title'")).get_attribute(
                'innerHTML').strip()

            hotel_price = float(deal_box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]')
                                .get_attribute('innerHTML')
                                .strip()
                                .split(';')[1]
                                .replace(',', '.'))

            review_element = deal_box.find_element(By.CSS_SELECTOR, "div[data-testid='review-score'] > div")
            review_score = None
            if review_element:
                try:
                    review_score = float(review_element.text.split('\n')[1])
                except ValueError:
                    print("Could not parse location score text:", review_element.text.split('\n')[1])

            # review_score = \
            # deal_box.find_element(By.CSS_SELECTOR, "div[data-testid='review-score'] > div").text.split('\n')[1]
            location_elements = deal_box.find_elements(By.CSS_SELECTOR,
                                                       'a[data-testid="secondary-review-score-link"] > span > span')
            location_score = None
            if location_elements:
                try:
                    location_score = float(location_elements[0].text.split(' ')[1])
                except ValueError:
                    print("Could not parse location score text:", location_elements[0].text)

            collection.append(
                    [hotel_name, hotel_price, review_score, location_score]
            )
        return collection
