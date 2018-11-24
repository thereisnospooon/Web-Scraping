from bs4 import BeautifulSoup
import requests


class Scraper:
    """
    An object that scrapes the given website
    """

    def __init__(self, path: str):
        """
        Constructor
        :param path: path to the website
        """
        self.path = path
        self.recipes = []

    def get_categories_urls(self):
        """
        Gets the urls from the main page of "www.allrecipes.com"
        :return:
        """
        urls = []
        source = requests.get(self.path).text
        soup = BeautifulSoup(source, 'lxml')
        links = soup.findAll('a')
        for tag in links:
            link = tag.get('href', None)
            if link is not None:
                urls.append(link)
        urls = self.filter_urls(urls)
        return urls

    def print_urls(self, main_content: list):
        """
        prints all the items in main content
        :param main_content: content to print
        :return:
        """
        for item in main_content:
            print(item)

    def is_recipe_url(self, param: str):
        """
        Given a url, this function assures that it's a valid url for a recipe
        :param param: the url
        :return: True if url is good False otherwise
        """
        if param.startswith("https://www.allrecipes.com/recipe/"):
            return True
        return False
        pass

    def filter_urls(self, urls):
        """
        Given an array of urls this function filters the ones that aren't recipes
        :param urls: the urls
        :return: only urls of recipes
        """
        out_urls = []
        for url in urls:
            if 'https://www.allrecipes.com/recipes' in url:
                out_urls.append(url)
        return out_urls

    def get_recipes(self):
        """
        :return: A list of recipes
        """
        recipe_urls = []
        category_urls = self.get_categories_urls()
        for url in category_urls:
            recipe_urls += self.scrape_ctegory_page(url)
        for url in recipe_urls:
            recipe_name, recipe_ings = self.scrape_url(url)
            self.recipes.append([recipe_name, url, recipe_ings])

    def scrape_url(self, url):
        """
        Given a recipe url, this method scrapes the recipe page for the ingredients needed.
        :param url: url for a recipe
        :return: a dictionary containing the recipe name, url, and ingredients needed.
        """
        rec_ingredients = []
        print("Now scraping: " + url)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        ingredients = soup.findAll("li", {"class": "checkList__line"})
        recipe_name_tag = soup.findAll("h1", {"id": "recipe-main-content"})
        recipe_name = recipe_name_tag[0].text
        for item in ingredients:
            if hasattr(item.label, "title"):
                rec_ingredients.append(item.label["title"])
        return recipe_name, rec_ingredients

    def scrape_ctegory_page(self, url):
        """
        Given a url to a category page of recipes, this method extracts the url of specific recipes
        :param url: url to category web page
        :return: the url's int this page
        """
        urls = []
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        divs = soup.findAll("div", {"class": "grid-card-image-container"})
        for div in divs:
            if hasattr(div.a, "href"):
                urls.append(div.a["href"])
        return urls


if __name__ == '__main__':
    scraper = Scraper("https://www.allrecipes.com/recipes/?page=2")
    scraper.get_recipes()
