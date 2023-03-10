'''
Code is written by Maxim Angel, aka Nakigoe
You can always find the newest version at https://github.com/nakigoe/linkedin-bot
contact me for Python and C# lessons at nakigoetenshi@gmail.com
$25 for 1 hour lesson
Put stars and share!!!
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.edge import service
import os
os.system("cls") #clear screen from previous sessions
import time

options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
my_service=service.Service(r'msedgedriver.exe')
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_experimental_option("detach", True)
options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage') # uses disk instead of RAM, may be slow

s = 20 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»

driver = webdriver.Edge(service=my_service, options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

text_file = open("message.txt", "r")
message = text_file.read()
text_file.close()

username = "nakigoetenshi@gmail.com"
password = "Super_Mega_Password"
login_page = "https://www.linkedin.com/login"
search_link = "https://www.linkedin.com/in/nakigoe"

def login():
    driver.get(login_page)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="username"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]'))).send_keys(password)
    action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Sign in")]')))).perform()

def scroll_to_bottom(): 
    reached_page_end= False
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    #expand the skills list:
    while not reached_page_end:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            reached_page_end = True
        else:
            last_height = new_height
            
def connect(name):
    try:
        #add note button:      
        action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Add a note"]')))).perform()
        
        #store the person's name and attach to the message:
        personalized_message = "Dear " + name + "\n" + message
        
        cover_letter_text = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@id="custom-message"]')))
        
        cover_letter_text.send_keys(personalized_message) 
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send now"]')))
        action.move_to_element(send_button).perform()
        time.sleep(0.5)
        action.click(send_button).perform()
        time.sleep(1)
        
    except TimeoutException:
        return 1           
    except StaleElementReferenceException:
        return 1
    except:
        return 1

def click_all_people_on_the_page():
    scroll_to_bottom()
    results = driver.find_elements(By.XPATH, '//div[@class="entity-result__item"]')
    for result in results:
        button_text = result.find_element(By.XPATH, './/span[@class="artdeco-button__text"]').get_attribute('innerHTML').strip("\n ")
        if button_text == "Pending":
            continue
        elif button_text == "Connect":
            person_button = result.find_element(By.XPATH, './/button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]')
            person_name = result.find_element(By.XPATH, './/span[@aria-hidden="true"]').get_attribute('innerHTML').strip("\n <!---->")
            action.move_to_element(person_button).perform()
            time.sleep(0.5)
            action.click(person_button).perform()
            time.sleep(1)
            connect(person_name)
        
def main():
    login()
    time.sleep(15)
    driver.get(search_link)
    action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="ember-view"]')))).perform()
    time.sleep(10)
    while True:
        try:
            time.sleep(10)
            test_results_presence = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="entity-result__item"]')))
        except TimeoutException:
            break
        except StaleElementReferenceException:
            break
        if test_results_presence:
            click_all_people_on_the_page()
        try:
            scroll_to_bottom()
            next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]')))
            action.move_to_element(next_page_button).perform()
            time.sleep(0.5)
            action.click(next_page_button).perform()
        except TimeoutException:
            break
        except StaleElementReferenceException:
            break

    # Close the only tab, will also close the browser.
    driver.close()
    driver.quit()
main()
