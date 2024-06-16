import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#---------------------------
# GET MEMOS TEXT FILE
#---------------------------

# TODO
# 1. Maybe login as a user so edits can be done quicker.

script_dir = os.path.dirname(os.path.realpath(__file__))

filename = "Google Keep 문서.txt"

file_path = os.path.join(script_dir, filename)

splitMemos = None

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read().replace('\\ufeff5', '')
    splitMemos = content.split('(next)')

print("Number of memos: ", len(splitMemos),"\n")

# remove trailing white space in each memo
for i in range(len(splitMemos)):
    splitMemos[i] = splitMemos[i].rstrip()

memo_dict = {}
for memo in splitMemos:
    memo = memo.lstrip().rstrip()
    lines = memo.split('\n')
    key = ' '.join(lines[:2])
    value = '\n'.join(lines[2:]).rstrip().lstrip()
    memo_dict[key] = value

# Function to extract the first number in a string
def extract_number(s):
    numbers = re.findall('\d+', s)
    return int(numbers[0]) if numbers else float('inf')

# Sort the dictionary in descending order
sorted_dict = {k: v for k, v in sorted(memo_dict.items(), key=lambda item: extract_number(item[0]), reverse=False)}

# Print the sorted dictionary
for key, value in sorted_dict.items():
    print(f'Key: {key}\nValue: {value}', "\n")

#-------------------------
# UPLOAD MEMOS TO HABANHA
#-------------------------
webdriver_service = Service('C:\\Program Files\\chromedriver-win64\\chromedriver.exe')

driver = webdriver.Chrome(service=webdriver_service)

# wait up to 10 seconds
wait = WebDriverWait(driver, 10)

#navigate to the posting site
driver.get('https://www.habanhatravelschool.com/77')

#navigate to memo upload form
xpath = "/html/body/div[6]/main/div/div[5]/div/div/div/div[2]/div[3]/div[2]"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

element.click()

for key, value in sorted_dict.items():
    #send name and password
    xpath = '//*[@id="post_form"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/span[1]/input'
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.send_keys("오유민")

    xpath = "/html/body/div[4]/div[3]/form/div[2]/div/div[2]/div[2]/div[1]/div[2]/span[2]/input"
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.send_keys("1234")

    #send title and memo body
    xpath = "/html/body/div[4]/div[3]/form/div[2]/div/div[2]/div[2]/div[1]/div[3]/div/input"
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.send_keys(key)

    xpath = "/html/body/div[4]/div[3]/form/div[2]/div/div[2]/div[2]/div[4]/div[1]/div/p"
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.send_keys(value)

    #click post
    xpath = '//*[@id="board_container"]/div[1]/div/div[2]/button'
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

    # navigate to post again
    xpath = '/html/body/div[6]/main/div/div[5]/div/div/div/div[2]/div/div/div/div[4]/div[2]/a[2]'
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

# navigate back to home class page
xpath = "/html/body/div[4]/div[1]/div/div[2]/a[1]"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()

time.sleep(600)