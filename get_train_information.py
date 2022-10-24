import re
from typing import List, Sequence, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_train_info(bf_soup: "BeautifulSoup", find_name: str="li") -> Sequence[List[str]]:
    trains = bf_soup.find_all(name=find_name)
    trains_contain_texts = []
    
    for train in trains:
        text = train.getText().replace("\n","")
        trains_contain_texts.append(text)
    
    trains_list = []
    for t in trains_contain_texts:
        if "[train]" in t:
            # print(t)
            train_name = t.replace("[line][train]","")
            trains_list.append(train_name)
    
    return trains_list


def get_time_info(bf_soup: "BeautifulSoup", find_name: str="li", class_name: str="time") -> Sequence[List[str]]:
    times = bf_soup.find_all(name=find_name, class_=class_name)
    time_list = []
    for time in times:
        # print(time.getText())
        time_list.append(time.getText().strip())
    
    train_number = len(get_train_info(bf_soup=bf_soup))
    
    departure_times = []
    arrival_times = []
    for time in time_list[:train_number]:
        time_pattern = "\d{2}:\d{2}"
        time_parts = re.findall(pattern=time_pattern, string=time)
        start = time_parts[0]
        end = time_parts[1]
        departure_times.append(start)
        arrival_times.append(end)
    
    return departure_times, arrival_times


def get_train_timetable(search_engine: "Selenium-webdriver") -> Tuple["Selenium-webdriver", Sequence[List[str]], List[str], List[str]]:        
    current_url = search_engine.current_url
    html = requests.get(current_url)
    soup = BeautifulSoup(html.content, "html.parser")   
    
    train_info = get_train_info(bf_soup=soup)
    train_depature_times, train_arrival_times = get_time_info(bf_soup=soup)

    return search_engine, train_info, train_depature_times, train_arrival_times


def convert_to_df(data: List) -> pd.DataFrame:
    df = pd.DataFrame()
    
    for n in range(len(data)):
        if n ==0:
            df['train'] = data[n][0]
            df['departure'] = data[n][1]
            df['arrival'] = data[n][2]
        else:
            _tmp = pd.DataFrame()
            _tmp['train'] = data[n][0]
            _tmp['departure'] = data[n][1]
            _tmp['arrival'] = data[n][2]
            df = pd.concat([df, _tmp])
            
    result_df = df.reset_index(drop=True)
    result_df = result_df.drop_duplicates()
    
    return result_df
