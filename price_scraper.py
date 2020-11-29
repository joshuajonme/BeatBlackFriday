import requests 
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils import convert_price_toNumber
import os

def scrape_amazon_search(search_term):
    URL = "http://www.amazon.com/"
    NUMBER_OF_PAGES_TO_SEARCH = 5
    PRODUCT_PATH = '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div'

    search_terms = search_term.split(" ")

    # Set ChromeDriver options
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    options.add_argument('--incognito')
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

    driver.get(URL)

    element = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    element.send_keys(search_term)
    element.send_keys(Keys.ENTER)

    products = []

    page = NUMBER_OF_PAGES_TO_SEARCH

    while True:
        if page != 0:
            try:
                driver.get(driver.current_url + "&page=" + str(page))
            except:
                break
        
        for i in driver.find_elements_by_xpath(PRODUCT_PATH):
            should_add = True
            name = ""
            price = ""
            prev_price = ""
            link = ""
            discount = 0.0
            # rating = ""
            prime = False
            try:
                h2tag = i.find_element_by_tag_name('h2')
                name = h2tag.text
                price = convert_price_toNumber(i.find_element_by_class_name('a-price').text)
                link = h2tag.find_element_by_tag_name('a').get_attribute("href")
                # rating = 
                try:
                    prime_element = i.find_element_by_class_name("a-icon-prime")
                    prime = True
                except:
                    Exception()
                try:
                    prev_price = convert_price_toNumber(i.find_element_by_class_name('a-text-price').text)
                    discount = (prev_price-price)/prev_price*100
                except:
                    Exception()
                    prev_price = price
            except:
                # print("exception")
                should_add = False
            
            product = {"Name": name, "Price": price, "Previous price": prev_price, 
                "Discount": discount, "URL": link, "Prime product": prime}
            if should_add:
                products.append(product)
                # print(products)
                
        page = page - 1
        if page == 0:
            break

        driver.quit()
    return products

        

def best_deal(products):
    biggest_discount = 0.0
    lowest_price = 0.0
    chepest_product = {}
    best_deal_product = {}

    run = 0
    for product in products:
        not_right = False
        # for word in search_terms:
        #     if word.lower() not in product.name.lower():
        #         not_right = True
        if not not_right:
            if run == 0:
                lowest_price = product["Price"]
                chepest_product = product
                run = 1
            elif product["Price"] < lowest_price:
                lowest_price = product["Price"]
                chepest_product = product
            if product["Discount"] > biggest_discount:
                biggest_discount = product["Discount"]
                best_deal_product = product

    return best_deal_product
    # with open('products.json', 'w') as json_file:
    #     data = []
    #     for prod in products:
    #         data.append(prod.serialize())
    #     json.dump(data, json_file, sort_keys=True, indent=4)

    # print(json.dumps(chepest_product.serialize(), indent=4, sort_keys=True))
    # print(json.dumps(best_deal_product.serialize(), indent=4, sort_keys=True))

    # options = get_web_driver_options()
    # set_ignore_certificate_error(options)
    # driver = get_chrome_web_driver(options)
    # driver.get(best_deal_product.link)
    # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')