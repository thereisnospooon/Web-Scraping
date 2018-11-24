from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.allrecipes.com').text
home_page = BeautifulSoup(source, 'lxml')
main_content = home_page.findAll('article', class_="fixed-recipe-card")

for item in main_content:
    print("*************************")
    print(item.prettify())
    print("*************************")
