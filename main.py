import argparse
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from get_train_information import (convert_to_df, get_time_info,
                                   get_train_info, get_train_timetable)
from interact_with_browser import InteractWithBrowser

url = "https://transit.yahoo.co.jp/"
browser = webdriver.Chrome()
browser.get(url)


def train_timetable_search(send_infos: List) -> List:
    
    data = [] # data of train information, departure and arrival time
    for i in range(len(search_hours)):
        
        # define the keyword to search using Selenium
        elements_search_input = ["query_input", "m", "d", "hh", "mm"]
        
        # i == 0: 最初の検索
        if i == 0:
            
            # interact_with_browser = InteractWithBrowser(engine=browser)
            
            for n, element in enumerate(elements_search_input):
                time.sleep(2)
                
                if element == "query_input":
                    ele = browser.find_elements("id", element)
                    # 出発
                    ele[0].send_keys(send_infos[0][0])
                    #　到着
                    time.sleep(1)
                    ele[1].send_keys(send_infos[0][1])
                
                elif element in ["m", "hh", "mm"]:
                    ele = browser.find_element("id", element)
                    ele.click()
                    ele.send_keys(send_infos[n])
                    ele.click()
                    
                else:
                    ele = browser.find_elements("id","d")[0]
                    ele.click()
                    ele.send_keys(send_infos[n])
                    ele.click()

            checked_box = True        
            if checked_box:
                check_boxes = ["air", "exp", "hbus", "bus", "fer"]
                for check_box in check_boxes:
                    time.sleep(1)
                    element_checkbox = browser.find_element("id",check_box)
                    element_checkbox.click()    
        
            # click search button
            interact_with_browser = InteractWithBrowser(engine=browser)
            interact_with_browser.click_search_bottom()
            
            # get current url and define new bf_soup
            current_url = browser.current_url
            html = requests.get(current_url)
            soup = BeautifulSoup(html.content, "html.parser")   
            
            # get train information and departure-arrival time
            train_info = get_train_info(bf_soup=soup)
            train_depature_times, train_arrival_times = get_time_info(bf_soup=soup)
        
            data.append([train_info, train_depature_times, train_arrival_times])
        
            browser.back()
            time.sleep(1)
        
        # ２回目の検索から
        if i != 0:
            
            # 検索入力
            interact_with_browser = InteractWithBrowser(engine=browser)
            interact_with_browser.next_search(search_hour=search_hours[i], search_min=search_min)
            interact_with_browser.click_search_bottom()
            
            # 検索エンジンお呼び電車の情報取得
            next_broswer, train_info, train_depature_times, train_arrival_times = get_train_timetable(search_engine=browser)

            data.append([train_info, train_depature_times, train_arrival_times])

            # 前の検索入力パージに戻す。その後で、順に次の散策を実施する
            next_broswer.back()
            time.sleep(1)
            
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str, help="出発駅")
    parser.add_argument("--end", type=str, help="到着駅")
    args = parser.parse_args()
    
    route_station = (args.start, args.end)
    
    # 検索の基本情報
    search_hours_start = 6 # 初めての電車は6時にする
    search_hours_finish = 22 # 終電は6時にする
    search_range = 2 # 2時間ずつ検索する
    search_month, search_day = "2月", "14日" # 2022年2月14日のみ検索する
    search_hours = [f"{h}時" for h in range(search_hours_start, search_hours_finish + search_range, search_range)]
    search_min = "00分"
    
    # 検索の情報をリストにまとめる
    input_search_information = [route_station, search_month, search_day, search_hours, search_min]
    
    # 結果取得
    search_results = train_timetable_search(send_infos=input_search_information)
    
    # pdに変換し、csvに保存する
    result_df = convert_to_df(search_results)
    result_df.to_csv(f"2022{search_month}{search_day}_{args.start}-{args.end}.csv", index=False)
    
    # print(result_df)
