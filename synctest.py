from selenium import webdriver
from selenium.webdriver.firefox.service import Service

fireFoxOpts = webdriver.firefox.options.Options()
fireFoxOpts.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
fireFoxOpts.add_argument('--profile')
fireFoxOpts.add_argument(r'C:\SeleniumProfile')

service = Service(r'C:\WebDrivers\geckodriver.exe')

driver = webdriver.Firefox(service=service, options=fireFoxOpts)

driver.get("https://read.amazon.com/notebook?ref_=kcr_notebook_lib&language=en-US")

x=input()
