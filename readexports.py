import quote
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.webdriver import FirefoxProfile

profile = 'C:\\Users\\natha\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\lzlso2cg.Selenium'
driver_path = "N:\Dev\webdrivers\geckodriver.exe"
print(profile)
email = ""
password = ""

# Opening JSON file
with open('settings.json') as json_file:
    data = json.load(json_file)
 
    # get email and pasword for settings
    email = data['email']
    password = data['password']

def main():
    print("Hello World!")

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument(r"--user-data-dir=C:\Users\natha\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    chromeOptions.add_argument(r'--profile-directory=C:\Users\natha\AppData\Local\Google\Chrome\User Data\Profile 1')
    #fireFoxOptions = webdriver.FirefoxOptions()
    #fireFoxOptions.add_argument('-headless')
    #fireFoxOptions.add_argument("-profile")
    #fireFoxOptions.add_argument(r'C:\Users\natha\AppData\Local\Mozilla\Firefox\Profiles\lzlso2cg.Selenium')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)

    driver.get("https://read.amazon.com/")
    assert "Kindle" in driver.title
    x=input()

    driver.find_element(By.ID, "top-sign-in-btn").click() #sign in on main page
    assert "Amazon Sign-In" in driver.title
    x=input()

    #login
    driver.find_element(By.ID, 'ap_email').send_keys(email)
    driver.find_element(By.ID, 'ap_password').send_keys(password)

    driver.find_element(By.NAME, 'rememberMe').click()

    driver.find_element(By.ID, 'signInSubmit').click()
    print(driver.current_url)

    x=input()
    # wait for the page to load and check if the login was successful
    time.sleep(5)
    if "Your Kindle Library" in driver.page_source:
        print("Login successful!")
    else:
        print("Login failed.")
        driver.quit()
        exit()
    x=input()

    # navigate to the "Your Highlights" page
    driver.get("https://www.amazon.com/kindle-dbs/h/myx")
    x=input()

    # wait for the page to load and expand all the sections to show all the highlights
    time.sleep(5)
    expand_buttons = driver.find_elements_by_xpath("//a[@class='a-expander-prompt']")
    for button in expand_buttons:
        button.click()
        time.sleep(1)
    x=input()

    # get all the highlights and save them to a text file
    highlights = driver.find_elements_by_class_name("kp-notebook-highlight")
    with open("kindle_highlights.txt", "w", encoding="utf-8") as f:
        for highlight in highlights:
            f.write(highlight.text + "\n")
    x=input()

    # print a message indicating the number of highlights that were saved to the text file
    print(f"Saved {len(highlights)} highlights to kindle_highlights.txt")
    x=input()

    # close the browser
    driver.quit()



if __name__ == "__main__":
    main()