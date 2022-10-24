import argparse
import os
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
    
    data = [] # 電車情報を保存するリスト
    for i in range(len(send_infos[3])): # send_infos[3]は検索時間(search_hour)
        
        # i == 0: 最初の検索
        if i == 0:
            
            interact_with_browser = InteractWithBrowser(engine=browser)
            
            # 検索情報をWebBrowserに送信する
            interact_with_browser.send_infos_to_browser(send_infos=send_infos)

            # 必要ない情報をチェックボークスを外す
            interact_with_browser.uncheck_checkbox()
        
            # 検索ボタンを押す
            interact_with_browser.click_search_bottom()
            
            # BeautifulSoupを用い、電車の情報、時間表を取得する
            current_url = browser.current_url
            html = requests.get(current_url)
            soup = BeautifulSoup(html.content, "html.parser")   
            # 電車の情報を取得する
            train_info = get_train_info(bf_soup=soup)
            train_depature_times, train_arrival_times = get_time_info(bf_soup=soup)
        
            data.append([train_info, train_depature_times, train_arrival_times])

            # 検索のページに戻す
            browser.back()
            time.sleep(1)
        
        # ２回目の検索から
        if i != 0:
            
            # 検索情報を入力する
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
    parser.add_argument("-D", "--departure_station", metavar="", type=str, help="出発駅")
    parser.add_argument("-A", "--arrival_station", metavar="", type=str, help="到着駅")
    args = parser.parse_args()
    
    route_station = (args.departure_station, args.arrival_station) # route_station例： ("東京","盛岡")
    
    # 検索の基本情報
    search_hours_start = 6 # 初めての電車は6時にする
    search_hours_finish = 10 # 終電の出発時間は22時にする
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
    
    output_file = "output"
    os.makedirs(output_file, exist_ok=False)
    result_df.to_csv(f"{output_file}/2022{search_month}{search_day}_{route_station[0]}-{route_station[1]}.csv", index=False)
    
    print(result_df)
    
