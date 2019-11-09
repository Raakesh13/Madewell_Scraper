import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re


def get_productDetails(url_list):
    base_url = 'https://www.madewell.com/'
    product_detail_list = []
    for url in url_list:
        product_details = dict()
        r = requests.get(url)

        product = BeautifulSoup(r.content, 'html.parser')
        product_main = product.find('div', {'class': 'product-main-content'})
        try:
            product_details['Name'] = product_main.find('h1', {'class': 'product-name'}).text
        except:
            product_details['Name']=None
        try:
            product_details['Price'] = product_main.find('div', {'class': 'product-usd'}).text.replace('\n', '')
        except:
            product_details['Price'] = None

        product_color = product_main.find('ul', {'class': 'swatches color'}).find_all('li')
        color_list = list()
        for color in product_color:
            try:
                color_list.append(color.find('a')['title'][14:])
            except:
                color_list = None
        product_details['Available_color'] = color_list
        image_src_list = []
        for img in product_main.find_all('div', {'class': 'product-images-desktop__column'}):
            image_src_list.append(img.find('img')['data-hires'])
        product_details['Image src list'] = image_src_list
        product_details['Product Description'] = product_main.find('li', {'class': 'a11yAccordionItem'}).find('div', {
            'class': 'a11yAccordionHideArea'}).text.replace('\n', '')
        sizes = []
        for size in product_main.find('ul', {'class': 'swatches size'}).find_all('li', {'class': 'selectable'}):
            sizes.append(size['data-value'])
        try:
            for size_type in product_main.find_all('li', {'class': 'extended-sizing-tile'}):
                if size_type.find('a')['href'] != 'javascript:;':
                    size_soup = BeautifulSoup(requests.get(base_url + size_type.find('a')['href'][1:]).content,
                                              'html.parser')
                    for size in size_soup.find('ul', {'class': 'swatches size'}).find_all('li',
                                                                                          {'class': 'selectable'}):
                        sizes.append(size['data-value'])
        except:
            pass
        product_details['Available sizes'] = sizes
        product_detail_list.append(product_details)
    return product_detail_list


def search_product(item_name):
    base_url = 'https://www.madewell.com/'
    product_url_list = []
    search_url = base_url+'search?q='+item_name
    r = requests.get(search_url)
    time.sleep(2)
    r_soup = BeautifulSoup(r.content, 'html.parser')
    result_count = re.findall('\d\d\d', r_soup.find('div', {'class': 'results-hits'}).text)[0]
    for i in range((int(result_count) // 36) + 1):
        items = requests.get(search_url + '&sz=36&start=' + str(36 * i) + '&format=page-element')
        items_soup = BeautifulSoup(items.content, 'html.parser')
        for product in items_soup.find_all('div', {'class': 'product-tile'}):
            product_url_list.append(base_url+product['data-monetate-producturl'][1:])

    return product_url_list


def navigate_product():
    product_url_list = []
    base_url = 'https://www.madewell.com/'
    driver = webdriver.Chrome(executable_path='/home/rakesh/Drivers/chromedriver_linux64/chromedriver')
    driver.header_overrides = {
        'Referer': 'User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
    }
    driver.get(base_url)
    driver.maximize_window()
    time.sleep(5)
    home_html = driver.execute_script('return document.documentElement.outerHTML')
    home_soup = BeautifulSoup(home_html, 'html.parser')
    try:
        driver.find_element_by_xpath("//select[@name='ddlCountry']/option[text()='United States']")
        driver.find_element_by_id('ipar_wmatcontinuebutton').send_keys(Keys.RETURN)
    except:
        pass
    for gender in home_soup.find('div', {'class': 'header-microsite-tabs'}).find_all('a')[:1]:
        driver.get(base_url + gender['href'][1:])
        gender_cat_html = driver.execute_script('return document.documentElement.outerHTML')
        gender_cat_soup = BeautifulSoup(home_html, 'html.parser')

        for category in gender_cat_soup.find('ul').find_all('a',
                                                            {'class': 'top-level-link has-sub-menu disabled-top-cat'})[
                        2:3]:
            driver.get(category['href'])
            subcat_html = driver.execute_script('return document.documentElement.outerHTML')
            subcat_soup = BeautifulSoup(subcat_html, 'html.parser')
            for item in subcat_soup.find_all('a', {'class': 'subcategory-nav__item-link'})[:1]:
                driver.get(item['href'])
                item_html = driver.execute_script('return document.documentElement.outerHTML')
                item_soup = BeautifulSoup(item_html, 'html.parser')
                result_count = re.findall('\d\d\d', item_soup.find('div', {'class': 'results-hits'}).text)[0]

                for i in range((int(result_count) // 36) + 1):
                    driver.get(item['href'] + '?sz=36&start=' + str(36 * i) + '&format=page-element')
                    product_html = driver.execute_script('return document.documentElement.outerHTML')
                    product_soup = BeautifulSoup(product_html, 'html.parser')
                    for product in product_soup.find_all('div', {'class': 'product-tile'}):
                        product_url_list.append(product['data-monetate-producturl'])
    driver.quit()
    return product_url_list

