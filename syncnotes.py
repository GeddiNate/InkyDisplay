import quote
import json
import time
import platform
import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# select chrome profile path based on which device im using
if platform.system() == 'Linux':
    profile = '/home/ngeddis/.config/google-chrome/Default' #Laptop
else:
    profile = 'C:\\Users\\natha\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1' #Desktop

# Opening JSON file
with open('settings.json') as json_file:
    data = json.load(json_file)
 
    # get email and password from settings
    email = data['email']
    password = data['password']

def main():
    #set chrome webdriver options
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument(f"--user-data-dir={profile}")
    #chromeOptions.add_argument(f'window-size=800,600')
    #print(f"--user-data-dir={profile}") #FOR TESTING
    
    #Start webdriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)

    #Go to kindle website
    driver.get("https://read.amazon.com/")
    time.sleep(5)

    #check if on landing page (not auto logged in)
    if "Amazon Kindle" in driver.title and "landing" in driver.current_url:
        print("On landing page")
        driver.find_element(By.ID, "top-sign-in-btn").click() #sign in on main page
        time.sleep(5)

        assert "Amazon Sign-In" in driver.title
        #if on sign in page attempt to sign in
        if "Amazon Sign-In" in driver.title:
            print("on Sign in page")
            # enter login info and submit
            driver.find_element(By.ID, 'ap_email').send_keys(email)
            driver.find_element(By.ID, 'ap_password').send_keys(password)

            driver.find_element(By.NAME, 'rememberMe').click()

            driver.find_element(By.ID, 'signInSubmit').click()
            time.sleep(5)

        #if 2FA required notify user
        if "Two-Step Verification" in driver.title:
            print(f"Manual 2FA required for {profile}")

    #wait for login
    time.sleep(5)
    if "kindle-library" in driver.current_url and "Kindle" in driver.title:
        print("Login successful!")
    #if log in failed notify user
    else:
        print("Login failed.")
        x=input()
        driver.quit()
        exit()

    #navigate to notes page
    driver.find_element(By.ID, 'notes_button').click()
    time.sleep(5)
    #opens in new tab
    driver.switch_to.window(driver.window_handles[1])

    #print(driver.find_element(By.ID, 'notes_button').get_attribute('href'))
    #time.sleep(10)

    if "Your Notes and Highlights" in driver.title:
        print("Reached Notes page successful")
        time.sleep(10)        

        library = driver.find_element(By.ID, 'kp-notebook-library')
        print(library.text)
        booklist = library.find_elements(By.CLASS_NAME, 'kp-notebook-library-each-book')
        
        
        
        tmp = library.text.splitlines()
        titles = []
        authors = []
        for item in tmp:
            if item.startswith("By:"):
                authors.append(item)
            else:
                titles.append(item)
        print(titles)
        print(authors)

        # for each book
        for book in booklist:
            #select the book so highlights and notes show on the page
            book.find_element(By.CLASS_NAME, 'a-link-normal').click()
            time.sleep(5)

            #find the notebook section of the page
            notebook = driver.find_element(By.ID, 'annotation-section')
            #get the data last accessed
            lastAccessed = notebook.find_element(By.ID, 'kp-notebook-annotated-date').text
            #TODO add a check if this date is more recent than the last sync date
            
            #get color of highlight
            colorsAndNumbers = []
            for color in notebook.find_elements(By.ID, 'annotationHighlightHeader'):
                colorsAndNumbers.append(color.text)
                #TODO add option to ignore highlights of a certain color

            #get page number
            notePage = []
            for note in notebook.find_elements(By.ID, 'annotationNoteHeader'):
                notePage.append(note.text)

            
            #get quote text
            quoteText = []
            for quote in notebook.find_elements(By.ID, 'highlight'):
                quoteText.append(quote.text)

            #get notes
            notes = []
            for note in notebook.find_elements(By.ID, 'note'):
                notes.append(note.text)
            
            
            print(lastAccessed)
            print(colorsAndNumbers)
            print(notePage)
            print(quoteText)
            print(notes)
    
    # id=annotationHighlightHeader contains quote color, page number
    # id=annotationNoteHeader contains note page number
    # id=highlight contains quote text
    # id="note" contains note text
    

    #library.

    #elements = driver.find_elements(By.CLASS_NAME, )
    #get list of books from sidebar
    #for each book check last accessed date
        #if book has been accessed since last sync
            #sync to stored data
            #record last sync date
            #write to file
    #exit browser
    #return to wait loop
    

    # #login
    # driver.find_element(By.ID, 'ap_email').send_keys(email)
    # driver.find_element(By.ID, 'ap_password').send_keys(password)

    # driver.find_element(By.NAME, 'rememberMe').click()

    # driver.find_element(By.ID, 'signInSubmit').click()
    # print(driver.current_url)

    # # wait for the page to load and check if the login was successful
    # time.sleep(5)
    # if "kindle-library" in driver.current_url:
    #     print("Login successful!")
    # else:
    #     print("Login failed.")
    #     driver.quit()
    #     exit()

    # # navigate to the "Your Highlights" page
    # driver.get("https://read.amazon.com/kindle-library")

    # # wait for the page to load and expand all the sections to show all the highlights
    # time.sleep(5)
    # expand_buttons = driver.find_elements_by_xpath("//a[@class='a-expander-prompt']")
    # for button in expand_buttons:
    #     button.click()
    #     time.sleep(1)

    # # get all the highlights and save them to a text file
    # highlights = driver.find_elements_by_class_name("kp-notebook-highlight")
    # with open("kindle_highlights.txt", "w", encoding="utf-8") as f:
    #     for highlight in highlights:
    #         f.write(highlight.text + "\n")

    # # print a message indicating the number of highlights that were saved to the text file
    # print(f"Saved {len(highlights)} highlights to kindle_highlights.txt")

    # close the browser
    x=input()
    driver.quit()


if __name__ == "__main__":
    main()