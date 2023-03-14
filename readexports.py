from bs4 import BeautifulSoup
import quote
import jsonpickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


email = ""
password = ""

def main():
    print("Hello World!")
    driver = webdriver.Firefox()
    driver.get("https://read.amazon.com/")
    assert "Kindle" in driver.title
    x = input()
    driver.find_element(By.ID, "top-sign-in-btn").click() #sign in on main page

    x = input()

    #login
    elem = driver.find_element(By.ID, 'ap_email')
    elem.send_keys(email)
    
    elem = driver.find_element(By.ID, 'ap_password')
    elem.send_keys(password)

    driver.find_element(By.NAME, 'rememberMe').click()

    driver.find_element(By.ID, 'signInSubmit')    

    







if __name__ == "__main__":
    main()