from library import Library
import json
import time
import logging
import datetime
import undetected_chromedriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from ast import literal_eval
import re


# strs to be removed from kindle date
DATE_FORMAT = "%A %B %d, %Y"

# time to wait for webpages to load
SLEEP_TIME = 5

DATA_FILE_PATH = "/srv/samba/highlights/"
TEST_FILE_PATH = ""

#
logging.basicConfig(filename='sync.log', encoding='utf-8', level=logging.DEBUG)

def loadSettings(settings_file="settings.json"):
    """
    Load user settings and credentials for syncing highlights

    return:
        Dictionary containing user settings
    """
    settings = {}
    with open(settings_file) as json_file:
        data = json.load(json_file)
        settings["profile"] = data["profile"]
        settings["colorsToSync"] = data["colorsToSync"]

    return settings

def syncKindleHighlights(library, settings):
    """
    Syncs local saved highlights with Kindle app only adds data updated since most recent sync.
    args:
        library: A BookList object containg all currently synced books and highlights.
        settings: A dictionary containing system settings.
    return: An updated libray containing new synced data 
    """

    logging.info("Begin Kindle sync")
    opts = Options()
    #opts.add_argument('--headless')

    # Start webdriver
    #driver = undetected_chromedriver.Chrome(options=opts)
    driver = undetected_chromedriver.Chrome()

    # Go to kindle website
    driver.get("https://read.amazon.com/")
    time.sleep(SLEEP_TIME) 
    try:
        # Load cookies from the JSON file and add them to the driver.
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    except:
        logging.warning("cookies.json file not found")

    if "Amazon Kindle" in driver.title and "landing" in driver.current_url:
        logging.info("Arrived on landing page")

        # click sign in button
        driver.find_element(By.ID, "top-sign-in-btn").click()
        time.sleep(SLEEP_TIME) # wait for loading

        # if on sign in page attempt to sign in
        if "Amazon Sign-In" in driver.title:
            logging.warn("Arrived on sign in page, credential entry required.")
        
            email = input("Amazon account email: ")
            password = input("Amazon account password: ")
            
            driver.find_element(By.ID, "ap_email").send_keys(email)
            driver.find_element(By.ID, "ap_password").send_keys(password)
            driver.find_element(By.NAME, "rememberMe").click()
            driver.find_element(By.ID, "signInSubmit").click()
            time.sleep(SLEEP_TIME) # wait for loading

        # if 2FA required notify user
        if "Two-Step Verification" in driver.title:
            logging.warning("2FA required.")
            print("Enter 2FA code:")
            otpcode=input()
            driver.find_element(By.ID, "auth-mfa-otpcode").send_keys(otpcode)
            driver.find_element(By.ID, "auth-mfa-remember-device").click()
            driver.find_element(By.ID, "auth-signin-button").click()
            time.sleep(SLEEP_TIME)
            
    # check if past login page
    if "kindle-library" in driver.current_url and "Kindle" in driver.title:
        logging.info("Login successful")
        # Dump cookies to JSON file.
        cookies = driver.get_cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)
    
    # if log in failed dump page source and exit
    else:
        logging.ERROR("Login failed, ending sync.")
        with open("html.json", 'w') as f: 
            f.write(driver.page_source)
        driver.quit()
        return library

    # navigate to notes page which opens in a new tab
    driver.find_element(By.ID, "notes_button").click()
    time.sleep(SLEEP_TIME)
    driver.switch_to.window(driver.window_handles[1])

    # Check if driver is on highlights page.
    if "Your Notes and Highlights" in driver.title:
        logging.info("Arrived on highlights page.")

        # get list of books from sidebar
        availible_books = driver.find_elements(By.CLASS_NAME, "kp-notebook-library-each-book")
        logging.info('Got list of books to sync.')

        for book in availible_books:
            selected_book = book.find_element(By.CLASS_NAME, "a-link-normal")
            selected_book.click()
            time.sleep(SLEEP_TIME)
            logging.info('Selected a book.')
        
            # get title and authors from the link
            tmp = re.split(r'[:\(\n]',selected_book.text)
            print(tmp)
            title = tmp[0].strip()
            subtitle = tmp[1].strip()
            authors = tmp[-1].split(' and ')

            if subtitle == 'By':
                subtitle = ''
            
            logging.info("Got authors, title and subtitle")

            # trim trailing whitespace 
            title = title.strip()

            # get the date the book was last accessed as python date object
            lastAccessed = datetime.datetime.strptime(driver.find_element(By.ID, "kp-notebook-annotated-date").text, DATE_FORMAT).date()
            logging.info('Got last accessed date')

            # sync all books that have been updated since last successful sync
            if lastAccessed > library.last_successful_sync:
                # sync new book data
                newBook = None
                # get number of of highlights in this book
                numHighlights = literal_eval(driver.find_element(By.ID, "kp-notebook-highlights-count").text)
                logging.info('Got number of highlights')
            
                # get highlight text, color and, notes
                highlightTexts = driver.find_elements(By.ID, "highlight")
                colors = driver.find_elements(By.ID, "annotationHighlightHeader")
                notes = driver.find_elements(By.ID, "note")
                logging.info('Got book data')

                # the color is the first word in the text
                colors = [color.text.split(" ", 1)[0] for color in colors]

                # add highlights to book object
                for i in range(numHighlights):
                    # if highlight contains an alert that the text cannot be displayed skip the highlight
                    if len(highlightTexts[i].find_elements(By.CLASS_NAME, 'a-alert-container')) !=0:
                        continue

                    # if color is in list of colors to sync
                    if colors[i] in settings["colorsToSync"]:
                        if newBook == None: #only create book if there is at least one quote to add
                            newBook = Book(title=title, authors=authors)
                        newBook.addHighlight(Highlight(text=highlightTexts[i].text, book=newBook, color=colors[i], note=notes[i].text))    

                # attempt to find book with matching title 
                # TODO books may have matching titles this will keep only one of those books check if subtitle and author matches as well
                # foundBook = library.findBook(title)
                # # if book already exist remove it
                # # TODO create a merge book method rather than replacing the book
                # if foundBook != None:
                #     library.removeBook(foundBook)
                if newBook != None:
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

    # Serialize cookies to JSON and save to a file
    cookies = driver.get_cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

    # close the browser
    #driver.quit()
    # update last successful sync to today
    library.lastSuccessfulSync = datetime.date.today()

    # return new data
    return library

def main():
    """Loads settings and book data, syncs data with kindle and Clippit, saves data
    """
    settings = loadSettings()
    library = Library()
    library.load()
    library = syncKindleHighlights(library, settings)
    # add sync from Clippit
    library.save()

if __name__=="__main__":
    main()