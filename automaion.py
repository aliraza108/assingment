from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import csv
from string import digits
data_file = "data.csv"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.leopardscourier.com/leopards-tracking")


with open('all.csv', "r", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        ID_tracking = ', '.join(row) 
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-control")))

        input_element = driver.find_element(By.CLASS_NAME, "form-control")
        input_element.send_keys(ID_tracking + Keys.ENTER)
        with open(data_file, "a+") as csvfile:   
            Current_statment = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]")
            table_of_Data = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr/td/table/tbody/tr[4]/td")
            Current_statment = Current_statment.text
            table_of_Data = table_of_Data.text
            dummytext = "active class not found"
            try:
                Status = driver.find_element(By.CLASS_NAME, "step-active")
                Dot_Status = Status.text
                if Dot_Status == "6\nDelivered":
                    Dot_Status = Dot_Status.replace("\n", "")
                    Dot_Status = ''.join([i for i in Dot_Status if not i.isdigit()])
                    dummytext = Dot_Status
                    
            except:
                print(dummytext)
            if Dot_Status == "Delivered":
                with open("data/delivered.csv", "a+") as deliveredfile:
                    csvwriter = csv.writer(deliveredfile)
                    tracking_row = [ID_tracking]
                    csvwriter.writerow(tracking_row)
            csvwriter = csv.writer(csvfile)
            rows = ID_tracking , dummytext , Current_statment
            csvwriter.writerow(rows)
  
time.sleep(100)
driver.quit()
print("bot done")

# arr = np.loadtxt("all.csv", delimiter=",", dtype=str)
# arr2 = np.loadtxt("delivered.csv", delimiter=",", dtype=str)

# with open("all.csv", "r+", newline='') as file:
#     file.truncate(0)
# # Remove delivered orders from all orders
# filtered_orders = [order for order in arr if order not in arr2]
# for a in filtered_orders:
#     # print(a) 
#     with open("all.csv", "a" , newline='') as newdata: 
#         print(a)
#         csvwriter = csv.writer(newdata)
#         csvwriter.writerow([a])

