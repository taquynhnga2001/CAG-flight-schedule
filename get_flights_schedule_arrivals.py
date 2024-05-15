from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

service = Service(executable_path="C:\\Users\\Hanna.Ta\\Projects\\plugshare-web-scraping\\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

driver.get("https://www.changiairport.com/en/flights/arrivals.html")
dates = ['Sunday, March 31st, 2024',
         'Monday, April 1st, 2024',
         'Tuesday, April 2nd, 2024',
         'Wednesday, April 3rd, 2024',
         'Thursday, April 4th, 2024',
         'Friday, April 5th, 2024',
         'Saturday, April 6th, 2024']
page_source = driver.page_source

soup = BeautifulSoup(page_source, features='html.parser')

arrival_df = pd.DataFrame(columns=['Date', 'Time', 'Flight Number', 'Airlines Name', 'Airport Name', 'Terminal', 'Boarding info', 'Status'])


for flight in soup.find_all('a', class_='flightlist__item display-lg')[1:]:
    print(flight.get_text())

    flight_time = flight.find('div', class_='flightlist__item-time').get_text()
    flight_time_prev = flight_time[:-5]
    flight_time = flight_time[-5:]
    print(f"{flight_time_prev} {flight_time}")

    flight_details = flight.find('div', class_='flightlist__item-flight').find('div', class_='airlines-details')
    flight_number = flight_details.find('span', class_='airport__flight-number').get_text()
    airlines_name = flight_details.find('span', class_='airport__name').get_text()
    airport_name = flight_details.find('div', class_='airport-name').get_text()
    print(f"{flight_number} {airlines_name} {airport_name}")

    flight_terminal = flight.find('div', class_='flightlist__item-terminal').get_text()
    boarding_info = flight.find('div', class_='flightlist__item-boarding').get_text()
    flight_status = flight.find('div', class_='flightlist__item-status').get_text()
    print(f"{flight_terminal} {boarding_info} {flight_status}")

    arrival_df = pd.concat([arrival_df, 
                            pd.DataFrame([{'Time': flight_time,
                                    'Flight Number': flight_number,
                                    'Airlines Name': airlines_name, 
                                    'Airport Name': airport_name, 
                                    'Terminal': flight_terminal, 
                                    'Boarding info': boarding_info, 
                                    'Status': flight_status}])
                            ], ignore_index=True)
    print()
 
arrival_df.to_csv('Arrivals.csv')   