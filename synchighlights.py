import highlight
import json
import time
import logging
import datetime
import undetected_chromedriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from ast import literal_eval

# strs to be removed from kindle date
DATE_FORMAT = "%A %B %d, %Y"

# time to wait for webpages to load
SLEEP_TIME = 5

#
logging.basicConfig(filename='sync.log', encoding='utf-8', level=logging.DEBUG)

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
    """function to sync local saved highlights with Kindle app only adds data since most recent sync

    :param BookList library: a BookList object containg all synced books and highlights
    :param dictionary settings: a dict containing system settings (requires profile, colors, email, password)
    :return BookList: an updated libray containing new synced data 
    """

    logging.info("Begin Kindle sync")

    #fireFoxOpts = webdriver.FirefoxOptions()
    opts = Options()
    #opts.add_argument(r'--user-data-dir=C:\Users\nathan.geddis\AppData\Local\Google\Chrome\User Data\Profile 2')
    opts.add_argument('--headless')

    profile = None
    if profile != None:
        opts.add_argument(f"--user-data-dir={profile}")

    # Start webdriver
    driver = undetected_chromedriver.Chrome(options=opts)

    # Go to kindle website
    driver.get("https://read.amazon.com/")
    time.sleep(SLEEP_TIME) # wait for loading

    # check if driver on kindle landing page (not auto logged in)
    if "Amazon Kindle" in driver.title and "landing" in driver.current_url:
        logging.info("Arrived on landing page")

        # click sign in button
        driver.find_element(By.ID, "top-sign-in-btn").click()
        time.sleep(SLEEP_TIME) # wait for loading

        # if on sign in page attempt to sign in
        if "Amazon Sign-In" in driver.title:
            logging.info("Arrived on sign in page")

            # enter login info, click remember me and submit
            driver.find_element(By.ID, "ap_email").send_keys(settings["email"])
            driver.find_element(By.ID, "ap_password").send_keys(settings["password"])
            driver.find_element(By.NAME, "rememberMe").click()
            driver.find_element(By.ID, "signInSubmit").click()
            time.sleep(SLEEP_TIME) # wait for loading

        # if 2FA required notify user
        if "Two-Step Verification" in driver.title:
            # TODO send notification if this is reached
            logging.warning("Manual 2FA required")
            print("Enter 2FA code:")
            otpcode=input()
            driver.find_element(By.ID, "auth-mfa-otpcode").send_keys(otpcode)
            driver.find_element(By.ID, "auth-mfa-remember-device").click()
            driver.find_element(By.ID, "auth-signin-button").click()
            time.sleep(SLEEP_TIME)
            
    # check if past login page
    if "kindle-library" in driver.current_url and "Kindle" in driver.title:
        logging.info("Login successful")
   
    # if log in failed notify user
    else:
        logging.ERROR("Login failed, ending sync")
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
        logging.info("Arrived on notes page")

        # get list of books from sidebar
        booklist = driver.find_elements(By.CLASS_NAME, "kp-notebook-library-each-book")
        logging.info('Got list of books to sync')

        # for each book (books are already sorted by most recently accessed)
        for book in booklist:
            # select link to highlights for this book
            selectedBook = book.find_element(By.CLASS_NAME, "a-link-normal")
            logging.info('Selected a book')
            
            # select the book so content is displayed
            selectedBook.click()
            time.sleep(SLEEP_TIME) # wait for loading
        
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
            logging.info("Got author and title")


            # get the date the book was last accessed as python date object
            lastAccessed = datetime.datetime.strptime(driver.find_element(By.ID, "kp-notebook-annotated-date").text, DATE_FORMAT).date()
            logging.info('Got last accessed date')

            # sync all books that have been updated since last successful sync
            if lastAccessed > library.lastSuccessfulSync:
                # sync new book data
                newBook = highlight.Book(title, author)
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
                    # if color is in list of colors to sync
                    if colors[i] in settings["colorsToSync"]:
                        newBook.addHighlight(highlight.Highlight(highlightTexts[i].text, colors[i], notes[i].text))    

                # attempt to find book with matching title 
                # TODO books may have matching titles this will keep only one of those books check if subtitle and author matches as well
                foundBook = library.findBook(title)
                # if book already exist remove it
                # TODO create a merge book method rather than replacing the book
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

    # close the browser
    driver.quit()
    # update last successful sync to today
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