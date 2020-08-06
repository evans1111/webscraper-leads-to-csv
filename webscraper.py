from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
from csv import DictWriter
import csv 
PATH = "C:\Windows\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Set Window Size
driver.set_window_size(1050, 1000)
# Open the website
driver.get("https://www.lpl.com/work-with-a-financial-professional/find-an-lpl-financial-professional.html?icid=M00297")

time.sleep(3)

# Locate the iFrame that contains the search form
iframe = driver.find_element_by_xpath("//*[@id='faaFrame']")

# Switch to the iFrame
driver.switch_to.frame(iframe)
time.sleep(3)

search = driver.find_element_by_id('address')
search.clear()
search.send_keys("Saint Petersburg, FL")
search.send_keys(Keys.RETURN)
time.sleep(3)

# Wait for a specific element to appear on the page
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='searchResultsContainer']/div[5]/div/a"))
        # EC.presence_of_all_elements_located((By.ID, "searchResultsContainer"))
    )
except:
    driver.quit()

# Gets the string that prints how many results were found
results = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='searchResultsContainer']/div[1]/div/p[1]"))
)

# 'Show More Results' Button
btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='searchResultsContainer']/div[5]/div/a"))
    )
# Get the string version of btn object
results_string = results.text

# Join the numbers together and add them to num_results array
num_results = [int(s) for s in results_string.split() if s.isdigit()]

# Locate the number within num_results array, and divide by 30 results per page to determine how many times to scroll + click
times_to_scroll = int(num_results[0] / 30)

# Scroll function will continue for as many times set within times_to_scroll
def scroll():
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        i = 1
        for i in range(i, (times_to_scroll + 1)):
            btn.click()
            print("button clicked!")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            i+1            

        # Check the length of the scroll position to determine when to break the while loop
        lastCount = lenOfPage
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        
        if lastCount==lenOfPage:
            match=True
            print("End of scroll!")      

scroll()

time.sleep(1)

# Get the name class element
names = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "name"))
    )

# Create a list of names
name_list = []
first_name_list = []
last_name_list = []
for name in names:
    name_list.append(name.text)
    name_arr = name.text.split(" ", 1)
    first_name_list.append(name_arr[0])
    last_name_list.append(name_arr[1]) if len(name_arr) > 1 else ""

# Get the email address element
emails = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "search-result-email"))
    )

# Create a list of emails
email_list = []
for email in emails:
    email_list.append(email.text) 

# Remove empty sets from beginning and end of email list  
email_list.pop(0)
email_list.pop(-1)

# Merge the three lists
contacts = list(zip(first_name_list, last_name_list, email_list))

a_file = open("results.csv", "w")
writer = csv.writer(a_file)
writer.writerow(["First Name", "Last Name", "Email"])
for fn, ln, e in contacts:
    writer.writerow([fn, ln, e])
    