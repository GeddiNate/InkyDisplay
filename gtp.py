import undetected_chromedriver as webdriver
import time
options = webdriver.ChromeOptions()
profile = "C:\\Users\\natha\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1'"
options.add_argument(f'user-data-dir={profile}')
driver = webdriver.Chrome(options=options, usersubprocess=True)
driver.get("https://read.amazon.com/")
time. sleep(100000)


