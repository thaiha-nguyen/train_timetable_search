# from selenium.webdriver.common.by import By
import time


class InteractWithBrowser():

    def __init__(self, engine: "Selenium-webdriver") -> None:
        self.engine = engine

    def next_search(self, search_hour: str, search_min: str) -> None:
        
        # search -> input hour
        time.sleep(2)
        element_hour = self.engine.find_element("id","hh")
        element_hour.click()
        element_hour.send_keys(search_hour)
        time.sleep(0.5)
        element_hour.click()
        
        # search -> input minute
        time.sleep(2)
        element_min = self.engine.find_element("id","mm")
        element_min.click()
        element_min.send_keys(search_min)
        time.sleep(0.5)
        element_min.click()
        

    def click_search_bottom(self) -> None:
        element_search_button = self.engine.find_element("id", "searchModuleSubmit")
        element_search_button.click()
