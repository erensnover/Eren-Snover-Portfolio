'''
Created a database from information taken from a public website through webscraping. I used the Selenium to open chrome, search to the specific page, retrieve the desired information, and create an organized and formatted Dataframe.
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
start_time = time.time()

driver = webdriver.Chrome()

final = pd.DataFrame()

print("1",time.time() - start_time)
thing=[]


for i in range(40):
    EST = pd.DataFrame()
    print(i," 2",time.time() - start_time)
    while True:
        driver.get('https://greenwich.ct.publicsearch.us/results?department=RP&limit=250&offset='+str(i*250)+'&parties=%7B%22parties%22%3A%5B%7B%22term%22%3A%22est%22%2C%22types%22%3A%5B%22grantor%22%2C%22grantee%22%5D%7D%5D%7D&recordedDateRange=18000101%2C19301030&searchType=advancedSearch&sort=desc&sortBy=recordedDate')
        try:
            WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/div/div[2]/div[1]/table/tbody/tr[50]/td[11]')))
            break
        except:
            print('error on this one')
    print(i," 3",time.time() - start_time)
    for j in range(4,11):
        print(i, " inner for loop",time.time() - start_time)
        elements = driver.find_elements(By.CLASS_NAME, 'col-'+str(j))
        EST[j]=pd.DataFrame(elements)[0].apply(lambda x: x.text)
    print(i," 4",time.time() - start_time)
    final=pd.concat([final,EST])


driver.quit()

final.columns = ['Book','Page','Grantor','Grantee','Doc Type','Property Address','Date']

final.to_excel("file path",sheet_name='sheet1')
