'''
2024-02-03 version, set CONNECT_WITH_NAME = False # Set to True in case you want to see the script in its true glory and burn through your monthly limit of personalized connection requests.
Code is written by Maxim Angel, aka Nakigoe
You can always find the newest version at https://github.com/nakigoe/linkedin-endorse-bot
contact me for Python and C# lessons at nakigoetenshi@gmail.com
Telegam: t.me/nakigoe
$60 for 1 hour lesson
Please place stars and share!!!
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import random
import os
import csv 
os.system("cls") #clear screen from previous sessions
import time
import json # for cookies
from urllib.parse import quote # to replace spaces and special characters in the URL

from enum import Enum # that one is for You, my dear reader, code readability from NAKIGOE.ORG
class Status(Enum):
    SUCCESS = 0
    FAILURE = 1

CONNECT_WITH_NAME = False # Set to True in case you want to see the script in its true glory and burn through your monthly limit of personalized connection requests
COOKIES_PATH = 'auth/cookies.json'
LOCAL_STORAGE_PATH = 'auth/local_storage.json'
user_agent = "My Standard Browser and Standard Device" # Replace with your desired user-agent string. You can find your current browser's user-agent by searching "What's my user-agent?" in a search engine
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_argument(f"user-agent={user_agent}")
options.add_experimental_option("detach", True)

s = 20 # static standard time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later», decrease the number if You do not use a VPN and have a high-speed Internet connection
driver = webdriver.Edge(options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

# Initialize global variables for csv file
current_profile_url = ""
current_message = ""
csv_file_path = "linkedin_connections_log.csv"

def custom_wait(driver, timeout, condition_type, locator_tuple):
    wait = WebDriverWait(driver, timeout)
    return wait.until(condition_type(locator_tuple))

number_of_messages=5
message = []
for i in range(number_of_messages): #the number of messages in the directory
    text_file = open("messages/linkedin-invitation-"+str(i)+".txt", "r")
    message.append(text_file.read())
    text_file.close()

username = "nakigoetenshi@gmail.com"
password = "Super Mega Password"
login_page = "https://www.linkedin.com/login"
max_char_length = 300 # the maximum length of the message to be sent, LinkedIn has a limit of 300 characters for the connect message (03.2024)

weekly_limit=200
weekly_limit -=5 # just for the sake of safety, besides, You want to be able to add some connections by hand!
weekly_counter = 0 #load from file!
text_file = open("linkedin-weekly-counter.txt", "r")
weekly_counter = int(text_file.readline())
text_file.close()

search_links_array = [] # these are just examples, you have top pick people from your contacts, who allowed to browse their contacts!!!
search_links_array.append("https://www.linkedin.com/in/barbara-stampf-81610029/") # Europe
search_links_array.append("https://www.linkedin.com/in/marlene-helml-9789681b9/") # Austrian lawyer
search_links_array.append("https://www.linkedin.com/in/mirko-serri-53ba085/") # Unicredit
search_links_array.append("https://www.linkedin.com/in/gerhard-heinz/") # somebody Austria international

# Define the list of locations without duplicates
uk_locations = ['London', 'Glasgow', 'Manchester', 'Birmingham', 'Bristol', 'Edinburgh', 'Leeds', 'Liverpool', 'Newcastle', 'Nottingham', 'Sheffield', 'Belfast', 'Brighton', 'Cardiff', 'Leicester', 'Bournemouth', 'Cambridge', 'Oxford', 'Reading', 'York', 'Aberdeen', 'Bath', 'Belfast', 'Birmingham', 'Bradford', 'Brighton', 'Bristol', 'Cambridge', 'Canterbury', 'Cardiff', 'Carlisle', 'Chester', 'Chichester', 'Coventry', 'Derby', 'Durham', 'Ely', 'Exeter', 'Gloucester', 'Hereford', 'Kingston upon Hull', 'Lancaster', 'Leeds', 'Leicester', 'Lichfield', 'Lincoln', 'Liverpool', 'City of London', 'Manchester', 'Newcastle upon Tyne', 'Norwich', 'Nottingham', 'Oxford', 'Peterborough', 'Plymouth', 'Portsmouth', 'Preston', 'Ripon', 'Salford', 'Salisbury', 'Sheffield', 'Southampton', 'St Albans', 'Stoke-on-Trent', 'Sunderland', 'Truro', 'Wakefield', 'Wells', 'Westminster', 'Winchester', 'Wolverhampton', 'Worcester', 'York']

us_locations = ['New York', 'New Orleans', 'Detroit', 'Los Angeles', 'San Francisco', 'Seattle', 'Chicago', 'Boston', 'Washington', 'Philadelphia', 'Houston', 'Dallas', 'Miami', 'Atlanta', 'Denver', 'Phoenix', 'San Diego', 'Minneapolis', 'Tampa', 'Orlando', 'Portland', 'Austin', 'Charlotte', 'Las Vegas', 'Nashville', 'Indianapolis', 'Columbus', 'San Antonio', 'Pittsburgh', 'Cincinnati', 'Kansas City', 'Sacramento', 'Cleveland', 'Milwaukee', 'St. Louis', 'Raleigh', 'Salt Lake City', 'Baltimore', 'Hartford', 'Buffalo', 'New Haven', 'Providence', 'Richmond', 'Oklahoma City', 'Louisville', 'Memphis', 'Jacksonville', 'Birmingham', 'Rochester', 'Tucson', 'Honolulu', 'Albuquerque', 'El Paso', 'Omaha', 'Allentown', 'Baton Rouge', 'Dayton', 'Tulsa', 'Worcester', 'Fresno', 'Syracuse', 'Albany', 'Bakersfield', 'Springfield', 'Toledo', 'Grand Rapids', 'Columbia', 'Greenville', 'Charleston', 'Wichita', 'Little Rock', 'Knoxville', 'Boise', 'Madison', 'Lakeland', 'Palm Bay', 'Pensacola', 'Cape Coral', 'Port St. Lucie', 'Naples', 'Sarasota', 'Ocala', 'Bridgeport', 'Newark', 'Wilmington', 'Winston-Salem', 'Greensboro', 'Reno', 'Spokane', 'Durham', 'Winston', 'Salem', 'Bakersfield', 'Stockton', 'Birmingham', 'Baton Rouge', 'Richmond', 'Des Moines', 'Harrisburg', 'Hartford', 'Jackson', 'Little Rock', 'Springfield', 'Columbia', 'Charleston', 'Wichita', 'Boise', 'Fargo', 'Sioux Falls', 'Billings', 'Cheyenne', 'Helena', 'Juneau', 'Honolulu', 'Anchorage', 'Fairbanks', 'Sitka', 'Ketchikan', 'Hilo', 'Kailua', 'Kapole']

linkedin_occupations = ['Academic Advisor', 'Accountant', 'Actor', 'Advocate', 'Alumni Relations Officer', 'Archeologist', 'Architect', 'Artist', 'Artistic Director', 'Astronomer', 'Auditor', 'Bank Teller', 'Biologist', 'Blogger', 'Botanist', 'Career Counselor', 'Carpenter', 'Chef', 'Chemist', 'Civic Engagement Leader', 'Coach', 'Community Health Worker', 'Community Manager', 'Consultant', 'Credit Analyst', 'Cultural Coordinator', 'Customer Service Representative', 'Dance Teacher', 'Data Analyst', 'Digital Content Creator', 'Ecologist', 'Economist', 'Editor', 'Education Consultant', 'Electrician', 'Engineer', 'Entrepreneur', 'Environmental Advocate', 'Events Organizer', 'Financial Advisor', 'Fitness Trainer', 'Freelancer', 'Fundraiser', 'Geologist', 'Graduate Assistant', 'Graphic Designer', 'Healthcare Assistant', 'Historian', 'Hospitality Manager', 'Influencer', 'Instructor', 'Insurance Agent', 'Interior Designer', 'Investment Banker', 'Journalist', 'Language Interpreter', 'Lecturer', 'Legal Advisor', 'Librarian', 'Marketing Assistant', 'Mechanic', 'Mentor', 'Meteorologist', 'Mortgage Advisor', 'Musician', 'Non-Profit Organizer', 'Nurse', 'Nutritionist', 'Outreach Coordinator', 'Personal Trainer', 'Photographer', 'Physicist', 'Physiotherapist', 'Plumber', 'Producer', 'Program Coordinator', 'Project Manager', 'Public Relations Officer', 'Publisher', 'Real Estate Agent', 'Research Assistant', 'Retail Manager', 'Risk Manager', 'SEO Specialist', 'Salesperson', 'Social Worker', 'Software Engineer', 'Sports Coach', 'Start-up Founder', 'Stock Broker', 'Student Ambassador', 'Student Union Officer', 'Sustainability Officer', 'Tax Consultant', 'Teacher', 'Theater Director', 'Tour Guide', 'Translator', 'Travel Blogger', 'Tutor', 'UX/UI Designer', 'Videographer', 'Volunteer Coordinator', 'Web Developer', 'Writer', 'Youth Worker']

custom_search_array = []

for location in uk_locations:
    for occupation in linkedin_occupations:
        custom_search_array.append(f"https://www.linkedin.com/search/results/people/?keywords={quote(occupation)}%20{quote(location)}&network=%5B%22S%22%5D")

links = custom_search_array if custom_search_array else search_links_array

def set_value_with_event(element, value):
    # Click to focus
    action = ActionChains(driver)
    action.move_to_element(element).click().perform()
    
    # Clear the existing value
    driver.execute_script("arguments[0].value = '';", element)
    
    # Use JavaScript to simulate human typing
    driver.execute_script("""
    var setValue = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    var element = arguments[0];
    var value = arguments[1];
    
    setValue.call(element, value);
    
    var event = new Event('input', { bubbles: true });
    element.dispatchEvent(event);
    """, element, value)

def click_and_wait(element, delay=1):
    action.move_to_element(element).click().perform()
    time.sleep(delay)
      
def scroll_to_bottom(delay=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            break
        last_height = new_height
        
def eternal_wait(driver, timeout, condition_type, locator_tuple): # timeout is symbolic here since it is eternal loop
    while True:
        try:
            element = custom_wait(driver, timeout, condition_type, locator_tuple)
            return element
        except:
            print(f"\n\nWaiting for the element(s) {locator_tuple} to become {condition_type}…")
            time.sleep(1) # just to display a message
            continue

def load_data_from_json(path): return json.load(open(path, 'r'))
def save_data_to_json(data, path): os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(data, open(path, 'w'))

def add_cookies(cookies): [driver.add_cookie(cookie) for cookie in cookies]
def add_local_storage(local_storage): [driver.execute_script(f"window.localStorage.setItem('{k}', '{v}');") for k, v in local_storage.items()]

def get_first_folder(path): return os.path.normpath(path).split(os.sep)[0] # for this to work, keep the cookies and localstorage in the same folder!

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            delete_folder(file_path) if os.path.isdir(file_path) else os.remove(file_path)
        os.rmdir(folder_path)

def success():
    try:
        eternal_wait(driver, 15, EC.presence_of_element_located, (By.XPATH, '//div[contains(@class,"global-nav__me")]'))
        return True
    except:
        return False

def navigate_and_check(probe_page):
    driver.get(probe_page)
    time.sleep(15)
    if success(): # return True if you are loggged in successfully independent of saving new cookies
        save_data_to_json(driver.get_cookies(), COOKIES_PATH)
        save_data_to_json({key: driver.execute_script(f"return window.localStorage.getItem('{key}');") for key in driver.execute_script("return Object.keys(window.localStorage);")}, LOCAL_STORAGE_PATH)
        return True
    else: 
        return False
   
def login():
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="username"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]'))).send_keys(password)
    action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Sign in")]')))).perform()
    time.sleep(15)
    
def check_cookies_and_login():
    driver.get(login_page) # you have to open some page first before trying to load cookies!
    time.sleep(3)
    
    if os.path.exists(COOKIES_PATH) and os.path.exists(LOCAL_STORAGE_PATH):
        add_cookies(load_data_from_json(COOKIES_PATH))
        add_local_storage(load_data_from_json(LOCAL_STORAGE_PATH))
        
        if navigate_and_check(links[0]): # just pick a first link to check if the cookies are OK
            return # it is OK, you are logged in
        else: # cookies outdated, delete them
            delete_folder(get_first_folder(COOKIES_PATH)) # please keep the cookies.json and local_storage.json in the same folder to clear them successfully (or delete the outdated session files manually)
    
    driver.get(login_page)
    time.sleep(3)
    login()
    navigate_and_check(links[0])
    
def truncate_name(name, max_length):
    if len(name) <= max_length:
        return name
    
    truncated = []
    remaining_length = max_length - 1  # -1 to reserve space for the ellipsis
    
    for word in name.split():
        if remaining_length - len(word) >= 0:
            truncated.append(word)
            remaining_length -= len(word) + 1  # +1 for the space or comma
        else:
            break
    
    if not truncated:  # The first name itself is too long
        return name[:max_length - 1] + "…"

    return " ".join(truncated) + "…"
            
def log_connection_attempt(name="N/A", has_message=False):
    global current_profile_url, current_message

    csv_file_path = "" 
    try:
        with open(csv_file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [name, current_profile_url, current_message if has_message else "N/A"]
            )
    except Exception as e:
        print("Failed to log connection attempt:", e)

def connect(name):
    try:
        try: # If LinkedIn is asking for an email which no one has, exit immediately! 
            email_demand = custom_wait(driver, 3, EC.presence_of_element_located, (By.XPATH, '//label[@for="email"]'))
            close_button = custom_wait(driver, 3, EC.element_to_be_clickable, (By.XPATH, '//button[@aria-label="Dismiss"]'))
            click_and_wait(close_button,0)
        except:
            pass
        
        try: # add a note button:
            add_a_note_button = custom_wait(driver, 5, EC.element_to_be_clickable, (By.XPATH, '//button[@aria-label="Add a note"]'))
            click_and_wait(add_a_note_button,0)
        except:
            pass #there are sometimes popups without THAT button
        
        try:
            cover_letter_textarea = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@id="custom-message"]')))
        except:
            return Status.FAILURE # if there is neither a button or a text area for a message, exit immediatly!
        
        message_text = message[random.randint(0,number_of_messages-1)]
        
        # sometimes a person name is too long, rectify it by delimeters, spaces, commas, etc:
        cleaned_name = truncate_name(name, max_char_length - len(message_text) - len("Dear ,\n")) # 300 is the current LinkedIn limit for the connect message (03.2024)
        
        #store the person's name and attach to the random message to reduce automation detection:
        personalized_message = f"Dear {cleaned_name},\n{message_text}"
        
        print(f"Length of the personalized_message: {len(personalized_message)}") #this is for debug
        
        set_value_with_event(cover_letter_textarea, personalized_message)
        
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send now"]')))
        action.click(send_button).perform()
        
        # close the irritating popup "You are growing your network", "You are approaching to the weekly limit", etc.
        try:
            got_it_button = custom_wait(driver, 2, EC.presence_of_element_located, (By.XPATH, '//button//span[contains(., "Got it")]'))
            click_and_wait(got_it_button,0)
        except:
            pass
        
        current_message = (personalized_message) # store the message for the log
        log_connection_attempt(name, True)  # log the connection attempt to csv file
        
        return Status.SUCCESS # OK, sent
    except:
        return Status.FAILURE
    
def connect_without_name():
    try:
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send now"]')))
        action.click(send_button).perform()
        
        log_connection_attempt()  # log the connection attempt to csv file
        
        # close the irritating popup "You are growing your network", "You are approaching to the weekly limit", etc.
        try:
            got_it_button = custom_wait(driver, 2, EC.presence_of_element_located, (By.XPATH, '//button//span[contains(., "Got it")]'))
            click_and_wait(got_it_button,0)
        except:
            pass
        
        return Status.SUCCESS # OK, sent
    except:
        return Status.FAILURE

def hide_header_and_messenger():    
    hide_header = wait.until(EC.presence_of_element_located((By.XPATH, '//header[@id="global-nav"]')))
    driver.execute_script("arguments[0].style.display = 'none';", hide_header)
    
    hide_top_menu = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'scaffold-layout-toolbar')))
    driver.execute_script("arguments[0].style.display = 'none';", hide_top_menu)
    
    hide_main_messenger = wait.until(EC.presence_of_element_located((By.XPATH, '//aside[@id="msg-overlay"]')))
    driver.execute_script("arguments[0].style.display = 'none';", hide_main_messenger)

def find_connect_buttons_and_people_names_and_perform_connect():
    global weekly_counter, current_profile_url
    scroll_to_bottom()
    time.sleep(3) #wait for the dynamic page to load
    
    try:
        connect_buttons = custom_wait(driver, 3, EC.presence_of_all_elements_located, (By.XPATH, '//button//span[contains(., "Connect")]'))
    except:
        return # That is a temporary solution if You target only those who have the "Connect" button
    
    hide_header_and_messenger()
    for connect_button in connect_buttons:
        person = connect_button.find_element(By.XPATH, './/ancestor::li[@class="reusable-search__result-container"]')
        person_name = person.find_element(By.XPATH, './/span[@dir="ltr"]//span[@aria-hidden="true"]').get_attribute('innerHTML').strip("\n <!---->")
        
        profile_link_element = person.find_element(By.XPATH, './/a[contains(@href, "/in/")]')  # the link to the person's profile
        current_profile_url = profile_link_element.get_attribute("href") # store the profile URL for the log
        
        click_and_wait(connect_button,0.5)
        
        if (weekly_counter<weekly_limit):
            # sts = connect(person_name)  # the MAIN part is in this function! Linkedin has limited the number of personalized messages to a non-existent number, so that functionality is temporarily disabled :_(
            if CONNECT_WITH_NAME == False:
                sts = connect_without_name()  # the MAIN part is in this function!
            else:
                sts = connect(person_name) # just in case you want to see the script in its True glory
            if sts == Status.FAILURE: continue
            elif sts == Status.SUCCESS:
                weekly_counter +=1
                with open('linkedin-weekly-counter.txt', 'w') as a:
                    a.writelines(str(weekly_counter))
                time.sleep(random.uniform(0.2, 2)) # to reduce LinkedIn automation detection
        elif(weekly_counter>=weekly_limit): # to reduce LinkedIn automation detection
            os.system("cls") #clear screen from unnecessary logs since the operation has completed successfully
            print("You've reached Your weekly limit of "+ str(weekly_limit) +" connection requests. Stop before LinkedIn blocks You! \n \nSincerely Yours, \nNAKIGOE.ORG\n")
            driver.close()
            driver.quit()
                
def main():
    check_cookies_and_login()
    
    for i, link in enumerate(links): 
        if i > 0: #fist link is already opened
            driver.get(link)
            eternal_wait(driver, 15, EC.presence_of_element_located, (By.XPATH, '//div[contains(@class,"global-nav__me")]')) # wait for the page to load
            
        if not custom_search_array: # that is, if you want to connect to the friend's friends, not the random custom search results
            action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="ember-view"]')))).perform()
            eternal_wait(driver, 15, EC.presence_of_element_located, (By.XPATH, '//div[contains(@class,"global-nav__me")]')) # wait for the page to load
        
        hide_header_and_messenger()
        
        # CSV file setup
        csv_headers = ["Name", "Profile URL", "Custom Message"]

        # Open the file in append mode, so we don't overwrite existing data
        with open(csv_file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            # If file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()
        
        while True:
            try:
                scroll_to_bottom()
                time.sleep(3)
                test_results_presence = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-view-name="search-entity-result-universal-template"]')))
            except:
                break
            if test_results_presence:
                #insert open «Follow» page function call here (if you write it)
                        
                #direct connect with the person's name included:
                find_connect_buttons_and_people_names_and_perform_connect()
            try:
                scroll_to_bottom()
                next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]')))
                action.move_to_element(next_page_button).perform()
                time.sleep(0.5)
                action.click(next_page_button).perform()
            except:
                break

    # Close the only tab, will also close the browser.
    driver.close()
    driver.quit()
main()