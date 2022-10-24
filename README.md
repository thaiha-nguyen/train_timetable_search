## How to run the code
### Prepare
* Installation
```shell
# selenium
pip install selenium

# beautifulsoup 
pip install beautifulsoup4

# chrome driver
brew install --cask chromedriver
```

### Run code
```shell
python main.py --start <出発駅> --end <到着駅>

```
* Example: 
    ```shell
    python main.py --departure_station 東京 --arrival_station 盛岡

    # OR
    python main.py -D 東京 -A 盛岡
    ```
