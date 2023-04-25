import highlight
import json
import time
import logging
import datetime
# import undetected_chromedriver as webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from ast import literal_eval

# strs to be removed from kindle date
DATE_FORMAT = "%A %B %d, %Y"

# time to wait for webpages to load
SLEEP_TIME = 5

def loadSettings():
    """Load user settings and crednetials for syncing highlights

    :return dictionary: contains browser profile, colors of highlights to sycn and login credentrials
    """
    # get settings from JSON file
    settings = {}
    with open("settings.json") as json_file:
        data = json.load(json_file)

        settings["profile"] = data["profile"]
        settings["colorsToSync"] = data["colorsToSync"]

    # get credentials for JSON file
    with open("credentials.json") as json_file:
        data = json.load(json_file)

        # get email and password from settings
        settings["email"] = data["email"]
        settings["password"] = data["password"]
    return settings

def syncKindleHighlights(library, settings):
    """function to sync local saved highlights with Kindle app

    :param BookList library: a BookList object containg all synced books and highlights
    :param dictionary settings: a dict containing system settings (requires profile, colors, email, password)
    :return BookList: an updated libray containing new synced data 
    """

    logging.info("Begin sync")



    #fireFoxOpts = webdriver.FirefoxOptions()
    fireFoxOpts = webdriver.firefox.options.Options()
    fireFoxOpts.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    fireFoxOpts.set_preference('profile', r'C:\SeleniumProfile')
    

    service = Service(r'C:\WebDrivers\geckodriver.exe')

    #fireFoxOpts.add_argument("--headless")

    profile = None
    if profile != None:
        fireFoxOpts.add_argument(f"--user-data-dir={profile}")

    # myProxy = "10.0.x.x:yyyy"
    # proxy = Proxy({
    # 'proxyType': ProxyType.MANUAL,
    #     'httpProxy': myProxy,
    #     'ftpProxy': myProxy,
    #     'sslProxy': myProxy,
    #     'noProxy': ''
    # })
    # driver = webdriver.Firefox(proxy=proxy)



    # # set chrome webdriver options
    # profile = settings["profile"]   
    # opts = webdriver.FirefoxOptions()
    # chromeOptions.add_argument('--no-sandbox')
    # 

    # Start webdriver
    #driver = webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver', service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)
    driver = webdriver.Firefox(service=service, options=fireFoxOpts)

    # Go to kindle website
    driver.get("https://read.amazon.com/")
    time.sleep(SLEEP_TIME) # wait for loading

    # check if driver on kindle landing page (not auto logged in)
    if "Amazon Kindle" in driver.title and "landing" in driver.current_url:
        print("On landing page")

        # click sign in button
        driver.find_element(By.ID, "top-sign-in-btn").click()
        time.sleep(SLEEP_TIME) # wait for loading

        # if on sign in page attempt to sign in
        if "Amazon Sign-In" in driver.title:
            print("on Sign in page")

            # enter login info, click remember me and submit
            driver.find_element(By.ID, "ap_email").send_keys(settings["email"])
            driver.find_element(By.ID, "ap_password").send_keys(settings["password"])
            driver.find_element(By.NAME, "rememberMe").click()
            driver.find_element(By.ID, "signInSubmit").click()
            time.sleep(SLEEP_TIME) # wait for loading

        # if 2FA required notify user
        if "Two-Step Verification" in driver.title:
            # TODO send notification if this is reached
            logging.warning(f"Manual 2FA required for {profile}")
            print("Enter 2FA code:")
            otpcode=input()
            driver.find_element(By.ID, "auth-mfa-otpcode").send_keys(otpcode)
            driver.find_element(By.ID, "auth-mfa-remember-device").click()
            driver.find_element(By.ID, "auth-signin-button").click()
            time.sleep(SLEEP_TIME)
            

    # check if past login page
    if "kindle-library" in driver.current_url and "Kindle" in driver.title:
        print("Login successful")
   
    # if log in failed notify user
    else:
        print("Login failed")
        # TODO send notification if this is reached
        driver.quit()
        return library

    # navigate to notes page
    driver.find_element(By.ID, "notes_button").click()
    time.sleep(SLEEP_TIME) # wait for loading

    # this opens in new tab so switch tabs
    driver.switch_to.window(driver.window_handles[1])

    # check if on highlights page
    if "Your Notes and Highlights" in driver.title:
        print("Reached Notes page successful")

        # get list of books from sidebar
        booklist = driver.find_elements(By.CLASS_NAME, "kp-notebook-library-each-book")
        print(booklist)
        print('got booklist')

        # for each book (books are already sorted by most recently accessed)
        for book in booklist:
            # select link to highlights for this book
            stuff = book.find_elements(By.CLASS_NAME, "a-link-normal")
            for thing in stuff:
                print(thing.get_attribute('outerHTML'))
            selectedBook = book.find_element(By.CLASS_NAME, "a-link-normal")
            print(selectedBook)
            print('got book')
        
            
            # get title and author from the link
            tmp = selectedBook.text.splitlines()
            title = tmp[0].strip()
            # remove By: from author string and leading space
            author = tmp[1][tmp[1].find(':') + 2:]

            # remove subtitle from title
            # TODO add subtitle support to highlight object
            indexs = (title.find(":"), title.find("(")) 

            # if ':' and '(' not found assume no subtitle
            if indexs[0] < 0 and indexs[1] < 0:
                title = title
            # if one of the values is negative (only one found)
            elif indexs[0] * indexs[1] < 0:
                # slice all text after the largest value
                title = title[:max(indexs[0], indexs[1])]
            # if both ':' and '(' found
            else:
                # slice all text after the first occurance
                title = title[:min(indexs[0], indexs[1])]
            
            # load Highlights for this book
            selectedBook.location_once_scrolled_into_view
            try:
                selectedBook.click()
            except Exception as e:
                print(e)
            driver.execute_script("arguments[0].click()",driver.find_element_by_id(ariticle_ids[0]))
            time.sleep(SLEEP_TIME) # wait for loading

            # get the date the book was last accessed as python date object
            lastAccessed = datetime.datetime.strptime(driver.find_element(By.ID, "kp-notebook-annotated-date").text, DATE_FORMAT).date()
            print('got last accessed')

            # sync all books that have been updated since last successful sync
            if lastAccessed > library.lastSuccessfulSync:
                # sync new book data
                newBook = highlight.Book(title, author)
                # get number of of highlights in this book
                numHighlights = literal_eval(driver.find_element(By.ID, "kp-notebook-highlights-count").text)
                print('got num highlights')
            
                # get highlight text, color and, notes
                highlightTexts = driver.find_elements(By.ID, "highlight")
                colors = driver.find_elements(By.ID, "annotationHighlightHeader")
                notes = driver.find_elements(By.ID, "note")
                print('got book data')

                # the color is the first word in the text
                colors = [color.text.split(" ", 1)[0] for color in colors]

                assert (numHighlights == len(colors) and numHighlights == len(highlightTexts) and numHighlights == len(notes))
                for i in range(numHighlights):
                    # if color is in list of colors to sync
                    if colors[i] in settings["colorsToSync"]:
                        newBook.addHighlight(highlight.Highlight(highlightTexts[i].text, colors[i], notes[i].text))
                

                # add book to library

                # attempt to find book with matching title 
                # TODO books may have matching titles this will keep only one of those books check if subtitle and author matches as well
                foundBook = library.findBook(title)
                # if book already exist remove it
                if foundBook != None:
                    library.removeBook(foundBook)
                library.addBook(newBook)
                

            # ==== Keeping this till TODO test a note without highlight in kindle
            # # get color of highlight
            # colors = []
            # for color in driver.find_elements(By.ID, "annotationHighlightHeader"):
            #     # color is the first word in text
            #     colors.append(color.text.split(" ", 1)[0])

            # # get highlight text
            # highlightText = []
            # for txt in driver.find_elements(By.ID, "highlight"):
            #     highlightText.append(txt.text)

            # # get notes
            # notes = []
            # for note in driver.find_elements(By.ID, "note"):
            #     notes.append(note.text)

            

  
    # id=annotationHighlightHeader contains highlight color, page number
    # id=annotationNoteHeader contains note page number
    # id=highlight contains highlight text
    # id="note" contains note text

    

    # close the browser
    driver.quit()
    library.lastSuccessfulSync = datetime.date.today()

    # return new data
    return library

def main():
    """Loads settings and book data, syncs data with kindle and Clippit, saves data
    """
    settings = loadSettings()
    library = highlight.BookList()
    library.load()
    library = syncKindleHighlights(library, settings)
    # add sync from Clippit
    library.save()

if __name__=="__main__":
    main()