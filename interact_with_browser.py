import time
from typing import Any, List, Optional, Tuple

elements_search_input = ["query_input", "m", "d", "hh", "mm"]


class SendingInformationType(List):
       route_station: Tuple[str]
       search_month: str
       search_day: str
       search_hours: List[str]
       search_min: str
           
       
class InteractWithBrowser():
    """Web Browserを作用するクラス"""
    
    def __init__(self, engine: Any, checked_box: Optional[bool]=True) -> None:
        self.engine = engine # Selenium webdriver
        self.checked_box = checked_box
        
    def send_infos_to_browser(self, send_infos: SendingInformationType) -> None:
        for n, element in enumerate(elements_search_input):
            time.sleep(2)    
            
            if element == "query_input":
                ele = self.engine.find_elements("id", element)
                # 出発駅の情報を入力する
                ele[0].send_keys(send_infos[0][0])
                # 到着の情報を入力する
                time.sleep(1)
                ele[1].send_keys(send_infos[0][1])
            
            elif element in ["m", "hh", "mm"]:
                ele = self.engine.find_element("id", element)
                ele.click()
                ele.send_keys(send_infos[n])
                ele.click()
                
            else:
                ele = self.engine.find_elements("id","d")[0]
                ele.click()
                ele.send_keys(send_infos[n])
                ele.click()

    def uncheck_checkbox(self) -> None:   
        if self.checked_box:
            check_boxes = ["air", "exp", "hbus", "bus", "fer"]
            for check_box in check_boxes:
                time.sleep(1)
                element_checkbox = self.engine.find_element("id",check_box)
                element_checkbox.click() 
                   
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
