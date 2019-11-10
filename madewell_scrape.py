import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas


# Function to get all product details from the list of urls of the products
def get_productDetails(product_url_list):
    base_url = 'https://www.madewell.com/'
    product_detail_list = []
    for url in product_url_list:
        product_details = dict()
        r = requests.get(url)

        product = BeautifulSoup(r.content, 'html.parser')
        product_main = product.find('div', {'class': 'product-main-content'})

        # Name of the product
        try:
            product_details['Name'] = product_main.find('h1', {'class': 'product-name'}).text
        except:
            product_details['Name'] = None

        # price of the product
        try:
            product_details['Price'] = product_main.find('div', {'class': 'product-usd'}).text.replace('\n', '')
        except:
            product_details['Price'] = None

        # Available Color of the product
        product_color = product_main.find('ul', {'class': 'swatches color'}).find_all('li')
        color_list = list()
        for color in product_color:
            try:
                color_list.append(color.find('a')['title'][14:])
            except:
                color_list = None
        product_details['Available_color'] = color_list

        # Image source of the product
        image_src_list = []
        for img in product_main.find_all('div', {'class': 'product-images-desktop__column'}):
            image_src_list.append(img.find('img')['data-hires'])
        product_details['Image src list'] = image_src_list

        # Description of the product
        product_details['Product Description'] = product_main.find('li', {'class': 'a11yAccordionItem'}).find('div', {
            'class': 'a11yAccordionHideArea'}).text.replace('\n', '')

        # Available sizes of the product
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


# function to get the url list when an item is searched
# Gender keywords for search_product() : men, women
def search_product(gender, item_name):
    base_url = 'https://www.madewell.com/'
    product_url_list = []
    search_url = base_url + 'search?q=' + item_name
    r = requests.get(search_url)
    r_soup = BeautifulSoup(r.content, 'html.parser')
    if gender == 'men':
        search_url = base_url + r_soup.find('div', {'class': 'see-other-results'}).find('p').find('a')['href'][1:]
        r = requests.get(search_url)
        r_soup = BeautifulSoup(r.content, 'html.parser')
    result_count = re.findall('\d+', r_soup.find('div', {'class': 'results-hits'}).text)[0]
    if gender == 'men':
        for i in range((int(result_count) // 36) + 1):
            items = requests.get(search_url + '&sz=36&start=' + str(36 * i) + '&format=page-element')
            items_soup = BeautifulSoup(items.content, 'html.parser')
            for product in items_soup.find_all('div', {'class': 'product-tile'}):
                product_url_list.append(product['data-monetate-producturl'])
    else:
        for i in range((int(result_count) // 36) + 1):
            items = requests.get(search_url + '&sz=36&start=' + str(36 * i) + '&format=page-element')
            items_soup = BeautifulSoup(items.content, 'html.parser')
            for product in items_soup.find_all('div', {'class': 'product-tile'}):
                product_url_list.append(base_url + product['data-monetate-producturl'][1:])
    return product_url_list


'''item keywords for navigate_product() for mens category: 
['New Arrivals', 'Best-Selling Styles', 'Current Rotation', 'Athletic Slim', 'The Outerwear Shop', 
'The Denim Digest', 'Custom Madewell', 'Jeans', 'Tees & Sweatshirts', 'Shirts', 'Jackets', 'Accessories', 'Shoes', 
'Shop All Jeans', 'Find Your Perfect Pair', 'Athletic Slim Fit Jeans', 'Skinny Jeans', 'Slim Jeans', 
'Straight Jeans', 'Denim Shirts', 'Denim Jackets', 'Shop All Do Well Styles', 'Recycle Your Jeans', '#DENIMMADEWELL', 
'Shop All Clothing', 'Sweaters', 'Pants', 'Shorts', 'Swim', 'Extended Sizes', 'Shop All Shoes', 'Sneakers', 'Boots', 
'Shop All Accessories', 'Bags', 'Scarves & Bandanas', 'Belts', 'Hats', 'Home', 'Socks', 'Sunglasses', 'Wallets and 
Accessories', 'Shop All Sale', 'Shop All Labels We Love', 'Carhartt Work in Progress', 'Champion', 'Madewell x 
Penfield', 'Mollusk', 'Vans', 'Veja', 'See All Inspo', 'Style', 'Community', 'Culture', 'Videos', 'See All Events', 
'Services', 'Locator', 'Our Initiatives', 'Our Partners', 'Our Materials', 'Our Community'] '''

'''item keywords for navigate_product() for womens category:
['New Arrivals', 'Looks We Love', 'Fall Collection', 'Find Your Perfect Pair', "Madewell Men's", 'The Outerwear 
Shop', 'Hometown Heroes', 'Best-Selling Styles', 'Shop All Do Well Styles', 'Custom Madewell', 'Fall Florals', 
'Stripe Hype', 'Cozy Sherpa & Fleece', 'Tomboy Plaid', 'Animal Print', 'Shop All Jeans', 'Skinny Jeans', 
'Curvy Jeans', 'Demi-Boot & Flare Jeans', 'Boyjeans', 'Perfect Vintage & Straight-Leg Jeans', 'Wide-Leg Jeans', 
'Overalls & Jumpsuits', 'Dresses', 'Jackets', 'Shirts', 'Shorts', 'Skirts', 'Maternity', 'Petite', 'Tall', 'Taller', 
'Fair Trade Denim', 'Rivet & Thread', "Men's Denim Digest", 'Recycle Your Jeans', '#denimmadewell', 'Shop All 
Clothing', 'Jeans', 'Sweaters', 'Tees', 'Tops & Shirts', 'Sweatshirts', 'Jackets & Coats', 'Pants', 'Active', 
'Intimates & Pajamas', 'Swim', 'Extended Sizes (Sizes 16-24)', 'The Office Hours Shop', 'Denim Dressing', 'Texture & 
Thread', 'Shop All Shoes', 'Boots', 'Flats', 'Heels', 'Mules & Slides', 'Oxfords & Loafers', 'Sneakers', 'Slippers', 
'Sandals', 'The Sneaker Shop', '#wellheeled', 'Shop All Accessories', 'Bags', 'Jewelry', 'Leather Accessories', 
'Scarves & Bandanas', 'Hats', 'Gloves', 'Sunglasses & Cases', 'Hair Accessories', 'Belts', 'Socks & Tights', 
'Brand-New Bag Straps', 'Statement Earrings', 'The Transport Collection', '#totewell', 'Shop All Life', 'Home', 
'Gift', 'Beauty', 'Candles', 'Shop All Labels We Love', 'See the Full List', 'Ace&Jig', 'Carhartt Work In Progress', 
'Evolg', 'Madewell x Penfield', 'Owen Barry', 'Vans', 'Veja', 'W&P', 'Wyeth', 'Hometown Heroes Collective', 
'Madewell x Dickies Collection', '25% Off Sweaters & Shoes', 'Extra 20% Off Sale Styles', 'Shop All Sale', 
'New to Sale', 'Sale Jeans', 'Sale Sweaters', 'Sale Jackets & Coats', 'Sale Tees', 'Sale Tops', 'Sale Dresses & 
Skirts', 'Sale Pants & Shorts', 'Sale Bags', 'Sale Shoes', 'Sale Jewelry', 'Sale Swim', 'See All Inspo', 'Style', 
'Community', 'Culture', 'Videos', 'See All Events', 'Services', 'Locator', 'Our Initiatives', 'Our Materials', 
'Our Partners', 'Our Community', '#everydaymadewell'] '''


# function to get the url list when an item selected from the navigation menu
# Gender keywords for navigate_product() : men, women

def navigate_product(gender, item):
    product_url_list = []
    base_url = 'https://www.madewell.com/'
    driver = webdriver.Chrome(executable_path='/home/rakesh/Drivers/chromedriver_linux64/chromedriver')

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

    if gender == 'men':
        driver.get(base_url + home_soup.find('div', {'class': 'header-microsite-tabs'}).find_all('a')[1]['href'][1:])
    home_html = driver.execute_script('return document.documentElement.outerHTML')
    home_soup = BeautifulSoup(home_html, 'html.parser')
    category_list = {}
    for category in home_soup.find_all('ul', {'class': 'level-2__subnav-group'}):
        for subcate in category.find_all('li'):
            category_list[subcate.find('a').text.replace('\n', '')] = subcate.find('a')['href']

    driver.get(category_list[item])
    item_html = driver.execute_script('return document.documentElement.outerHTML')
    item_soup = BeautifulSoup(item_html, 'html.parser')

    result_count = re.findall(r'\d+', item_soup.find('div', {'class': 'results-hits'}).text)[0]

    for i in range((int(result_count) // 36) + 1):
        driver.get(category_list[item] + '?sz=36&start=' + str(36 * i) + '&format=page-element')
        product_html = driver.execute_script('return document.documentElement.outerHTML')
        product_soup = BeautifulSoup(product_html, 'html.parser')
        for product in product_soup.find_all('div', {'class': 'product-tile'}):
            product_url_list.append(product['data-monetate-producturl'])

    driver.quit()
    return product_url_list


