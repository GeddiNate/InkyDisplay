import quote
import json
import time
import logging
import datetime
import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from ast import literal_eval

# strs to be removed from kindle date
DATE_FORMAT = "%A %B %d, %Y"

# time to wait for webpages to load
SLEEP_TIME = 7


def syncQuotes(library, settings):
    """function to sync local saved quotes with Kindle app

    :param BookList library: a BookList object containg all synced books and quotes
    :param dictionary settings: a dict containing system settings (requires profile, colors, email, password)
    :return BookList: an updated libray containing new synced data 
    """

    logging.info("Begin sync")

    # set chrome webdriver options
    profile = settings["profile"]   
    chromeOptions = webdriver.ChromeOptions()
    if profile != None:
        chromeOptions.add_argument(f"--user-data-dir={profile}")

    # Start webdriver
    #driver = webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver', service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)
    driver = webdriver.Chrome(options=chromeOptions)

    # Go to kindle website
    driver.get("https://read.amazon.com/")
    time.sleep(SLEEP_TIME) # wait for loading

    # check if driver on kindle landing page (not auto logged in)
    if "Amazon Kindle" in driver.title and "landing" in driver.current_url:
        logging.info("On landing page")

        # click sign in button
        driver.find_element(By.ID, "top-sign-in-btn").click()
        time.sleep(SLEEP_TIME) # wait for loading

        # if on sign in page attempt to sign in
        if "Amazon Sign-In" in driver.title:
            logging.info("on Sign in page")

            # enter login info, click remember me and submit
            driver.find_element(By.ID, "ap_email").send_keys(settings["email"])
            driver.find_element(By.ID, "ap_password").send_keys(settings["password"])
            driver.find_element(By.NAME, "rememberMe").click()
            driver.find_element(By.ID, "signInSubmit").click()
            time.sleep(SLEEP_TIME) # wait for loading

        # if 2FA required notify user
        if "Two-Step Verification" in driver.title:
            logging.warn(f"Manual 2FA required for {profile}")
            x=input() # FOR TESTING ONLY REMOVE BEFORE RELEASE
            # TODO send notification if this is reached

    # check if past login page
    if "kindle-library" in driver.current_url and "Kindle" in driver.title:
        logging.info("Login successful")
   
    # if log in failed notify user
    else:
        logging.error("Login failed")
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
        logging.info("Reached Notes page successful")

        # get list of books from sidebar
        booklist = driver.find_elements(By.CLASS_NAME, "kp-notebook-library-each-book")

        # for each book (books are already sorted by most recently accessed)
        for book in booklist:
            # select link to highlights for this book
            selectedBook = book.find_element(By.CLASS_NAME, "a-link-normal")
            
            # get title and author from the link
            tmp = selectedBook.text.splitlines()
            title = tmp[0].strip()
            # remove By: from author string and leading space
            author = tmp[1][tmp[1].find(':') + 2:]

            # remove subtitle from title
            # TODO add subtitle support to quote object
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
            selectedBook.click()
            time.sleep(SLEEP_TIME) # wait for loading

            # get the date the book was last accessed as python date object
            lastAccessed = datetime.datetime.strptime(driver.find_element(By.ID, "kp-notebook-annotated-date").text, DATE_FORMAT).date()

            # sync all books that have been updated since last successful sync
            if lastAccessed > library.lastSuccessfulSync:
                # sync new book data
                newBook = quote.Book(title, author)
                # get number of of highlights in this book
                numHighlights = literal_eval(driver.find_element(By.ID, "kp-notebook-highlights-count").text)
            
                # get quote text, color and, notes
                quoteTexts = driver.find_elements(By.ID, "highlight")
                colors = driver.find_elements(By.ID, "annotationHighlightHeader")
                notes = driver.find_elements(By.ID, "note")

                # the color is the first word in the text
                colors = [color.text.split(" ", 1)[0] for color in colors]

                assert (numHighlights == len(colors) and numHighlights == len(quoteTexts) and numHighlights == len(notes))
                for i in range(numHighlights):
                    # if color is in list of colors to sync
                    if colors[i] in settings["colorsToSync"]:
                        newBook.addQuote(quote.Quote(quoteTexts[i].text, colors[i], notes[i].text))
                

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

            # # get quote text
            # quoteText = []
            # for txt in driver.find_elements(By.ID, "highlight"):
            #     quoteText.append(txt.text)

            # # get notes
            # notes = []
            # for note in driver.find_elements(By.ID, "note"):
            #     notes.append(note.text)

            

  
    # id=annotationHighlightHeader contains quote color, page number
    # id=annotationNoteHeader contains note page number
    # id=highlight contains quote text
    # id="note" contains note text

    

    # close the browser
    driver.quit()
    library.lastSuccessfulSync = datetime.date.today()

    # return new data
    return library
