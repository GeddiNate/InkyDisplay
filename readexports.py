from bs4 import BeautifulSoup
import quote

f = open('Exports/The Way of Kings (The Stormlight Archive, Book 1)-Notebook.html', 'r', encoding="utf-8") 

soup = BeautifulSoup(f, 'html.parser')


print(soup.prettify())