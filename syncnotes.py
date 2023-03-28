import quote
import json
import time
import platform
import logging
import datetime
import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from ast import literal_eval

# strs to be removed from kindle date
DAYS = [
    "Monday ",
    "Tuesday ",
    "Wednesday ",
    "Thursday ",
    "Friday ",
    "Saturday ",
    "Sunday ",
]

# time to wait for webpages to load
SLEEP_TIME = 7

# function to sync local saved quotes with Kindle app
def syncQuotes(data, settings):

    # set chrome webdriver options
    profile = settings["profile"]   
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument(f"--user-data-dir={profile}")

    # Start webdriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)

    # Go to kindle website
    driver.get("https://read.amazon.com/")
    time.sleep(SLEEP_TIME)

    # check if on landing page (not auto logged in)
    if "Amazon Kindle" in driver.title and "landing" in driver.current_url:
        logging.info("On landing page")

        # click sign in button
        driver.find_element(By.ID, "top-sign-in-btn").click()
        time.sleep(SLEEP_TIME)

        # if on sign in page attempt to sign in
        if "Amazon Sign-In" in driver.title:
            logging.info("on Sign in page")

            # enter login info, click remember me and submit
            driver.find_element(By.ID, "ap_email").send_keys(settings["email"])
            driver.find_element(By.ID, "ap_password").send_keys(settings["password"])
            driver.find_element(By.NAME, "rememberMe").click()
            driver.find_element(By.ID, "signInSubmit").click()
            time.sleep(SLEEP_TIME)

        # if 2FA required notify user
        if "Two-Step Verification" in driver.title:
            print(f"Manual 2FA required for {profile}")
            # TODO send notification if this is reached

    # check if past login page
    if "kindle-library" in driver.current_url and "Kindle" in driver.title:
        logging.info("Login successful")
    # if log in failed notify user
    else:
        logging.error("Login failed")
        # TODO send notification if this is reached
        driver.quit()
        return


    # navigate to notes page
    driver.find_element(By.ID, "notes_button").click()
    time.sleep(SLEEP_TIME)

    # this opens in new tab so switch tabs
    driver.switch_to.window(driver.window_handles[1])

    # check if on highlights page
    if "Your Notes and Highlights" in driver.title:
        logging.info("Reached Notes page successful")

        library = driver.find_element(By.ID, "kp-notebook-library")
        booklist = library.find_elements(By.CLASS_NAME, "kp-notebook-library-each-book")
        
        books = []
        # for each book
        for book in booklist:
            # select the book so highlights and notes show on the page
            selectedBook = book.find_element(By.CLASS_NAME, "a-link-normal")
            
            # contains title and author
            tmp = selectedBook.text.splitlines()
            
            # remove subtitle if there
            idx = max(tmp[0].find(":"), tmp[0].find("("))
            # TODO this won't work if a title has : and ( hasn't been a problem yet but might be
            if idx < 0:
                title = (tmp[0])
            else:
                title = (tmp[0][:idx])
            
            author = tmp[1]

            selectedBook.click()
            time.sleep(5)
            
            # find the notes page

            
            # get number of of highlights in this book
            numHighlights = literal_eval(driver.find_element(By.ID, "kp-notebook-highlights-count").text)

            # find the notebook section of the page
            notebook = driver.find_element(By.ID, "annotation-section")

            # get the date the book was last accessed
            lastAccessed = notebook.find_element(By.ID, "kp-notebook-annotated-date").text
            
            # remove day of the week from last accessed date
            for day in DAYS:
                lastAccessed = lastAccessed.replace(day, "")
            # TODO add a check if this date is more recent than the last sync date

            # get color of highlight
            colors = []
            for color in notebook.find_elements(By.ID, "annotationHighlightHeader"):
                # color is the first word in text
                colors.append(color.text.split(" ", 1)[0])
                # TODO add option to ignore highlights of a certain color

            # get quote text
            quoteText = []
            for txt in notebook.find_elements(By.ID, "highlight"):
                quoteText.append(txt.text)

            # get notes
            notes = []
            for note in notebook.find_elements(By.ID, "note"):
                notes.append(note.text)

            assert (numHighlights == len(colors)
                    and numHighlights == len(quoteText)
                    and numHighlights == len(notes))
            b = quote.Book(title, author, lastAccessed)
            for i in range(numHighlights):
                b.quotes.append(quote.Quote(quoteText[i], colors[i], notes[i]))
            books.append(b)
            
    # id=annotationHighlightHeader contains quote color, page number
    # id=annotationNoteHeader contains note page number
    # id=highlight contains quote text
    # id="note" contains note text


    # close the browser
    with open("output.json", "w") as json_file:
        json_file.write(json.dumps(books, default=vars))
    driver.quit()

