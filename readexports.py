from bs4 import BeautifulSoup

f = open('Exports/The Way of Kings (The Stormlight Archive, Book 1)-Notebook.html', 'r') 

soup = BeautifulSoup(f, 'html.parser')


print(soup.prettify())