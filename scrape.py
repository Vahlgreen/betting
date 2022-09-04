import selenium
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os



#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('headless')
#chrome_options.add_argument('window-size=1920x1080')
#chrome_options.add_argument("disable-gpu")
#driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.flashscore.dk/fodbold/danmark/superliga-2021-2022/resultater/")
time.sleep(1)
driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div/div[1]/div/div[2]/div/button[2]').click() #  cookies
driver.execute_script("window.scrollBy(0,10000)", "")
time.sleep(1)
driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/div/div/main/div[4]/div[2]/div[1]/div[1]/div/div/a").click() #hvis flere kampe
time.sleep(1)
driver.execute_script("window.scrollBy(0,5000)", "")

print(driver.find_element(By.CSS_SELECTOR,"div.event__participant.event__participant--home.fontExtraBold").text)
print(driver.find_element(By.CSS_SELECTOR,'div.event__participant.event__participant--home').text)
print(driver.find_element(By.CSS_SELECTOR,'div.event__participant.event__participant--home').text)

i=1
my_dict = {"date":[],"home_team":[],"away_team":[], "home_score":[], "away_score":[],"home_odds":[],"draw_odds":[],"away_odds":[]}
while i<=285:
    try:



        date = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div/div/main/div[4]/div[2]/div[1]/div[1]/div/div/div[{i}]/div[1]').text
        home_team = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div/div/main/div[4]/div[2]/div[1]/div[1]/div/div/div[{i}]/div[2]').text
        away_team = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div/div/main/div[4]/div[2]/div[1]/div[1]/div/div/div[{i}]/div[3]').text
        home_score = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div/div/main/div[4]/div[2]/div[1]/div[1]/div/div/div[{i}]/div[4]').text
        away_score = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div/div/main/div[4]/div[2]/div[1]/div[1]/div/div/div[{i}]/div[5]').text

        match_element = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div/div/main/div[4]/div[2]/div[1]/div[1]/div/div/div[{i}]') #find kamp
        #driver.execute_script("arguments[0].scrollIntoView()", match_element) #scroll til kamp

        time.sleep(0.5)
        match_element.click() #click på kamp


        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        main_handle = driver.current_window_handle

        for handle in driver.window_handles:
            if handle != main_handle:
                driver.switch_to.window(handle)

        driver.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/a[2]').click() #click på odds
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div[2]/a[2]').click() #click på 1. halvleg
        time.sleep(1)


        home_odds = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div[3]/div/div[2]/div[1]/a[1]/span').text
        draw_odds = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div[3]/div/div[2]/div[1]/a[2]/span').text
        away_odds = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div[3]/div/div[2]/div[1]/a[3]/span').text

        driver.close()
        driver.switch_to.window(main_handle)
        if i%5 == 0:
            driver.execute_script("window.scrollBy(0,-300)", "")

        print(f"{date}: {home_team} vs {away_team} ({home_score}-{away_score}): ODDS: 1: {home_odds} x: {draw_odds} 2: {away_odds}")
        my_dict["date"].append(date)
        my_dict["home_team"].append(home_team)
        my_dict["away_team"].append(away_team)
        my_dict["home_score"].append(home_score)
        my_dict["away_score"].append(away_score)
        my_dict["home_odds"].append(home_odds)
        my_dict["draw_odds"].append(draw_odds)
        my_dict["away_odds"].append(away_odds)
        i=i+1
    except Exception as er:
        print("exception")
        i=i+1
        continue



pd.DataFrame.from_dict(my_dict).to_csv("fodbold.csv",index=False)

test = "hej"


