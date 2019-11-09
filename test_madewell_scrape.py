import unittest
from madewell_scrape import *

url_list = []

base_url = 'https://www.madewell.com/'

product_search_shirts = [{'Name': 'Baum Und Pferdgarten Maiko Puff-Sleeve Top',  'Price': 'Sale Price$199.00', 'Available_color': ['PEACH FLOWER']}, {'Name': 'Baum Und Pferdgarten Aubree Tie-Waist Shirt', 'Price': 'Sale Price$199.00', 'Available_color': ['WARM SAND']}]
product_search_jeans = [{'Name': 'The Petite High-Rise Slim Boyjean in Lunar Wash',  'Price': 'Sale Price$128.00', 'Available_color': ['LUNAR WASH']}, {'Name': 'The Petite Perfect Vintage Jean in Ainsworth Wash', 'Price': 'Sale Price$128.00', 'Available_color': ['AINSWORTH WASH']}]

product_nav_list = ['https://www.madewell.com/10%22-high-rise-skinny-jeans-in-berkeley-black-button-through-edition-AA590.html?dwvar_AA590_color=DM1895&cgid=apparel-jeans',
                    'https://www.madewell.com/roadtripper-jeans-in-jansen-wash-K1877.html?dwvar_K1877_color=DM2729&cgid=apparel-jeans',
                    'https://www.madewell.com/roadtripper-jeans-in-bennett-black-G7392.html?dwvar_G7392_color=DM1744&cgid=apparel-jeans']
 
search_result_list = ['https://www.madewell.com/evercrest-turtleneck-sweater-in-coziest-yarn-AF506.html?color=NA0140',
                      'https://www.madewell.com/brockton-bobble-sweater-in-coziest-yarn-AF097.html?color=SU4133',
                      'https://www.madewell.com/cashmere-mockneck-sweater-K1612.html?color=GR0068',
                      'https://www.madewell.com/buffalo-check-kent-cardigan-sweater-in-coziest-yarn-AF514.html?color=SU3380',
                      'https://www.madewell.com/colorblock-midi-sweater-dress-in-coziest-yarn-AF161.html?color=SU3425',
                      'https://www.madewell.com/the-clair-lace-up-boot-in-shearling-lined-suede-AE237.html?color=BR7079',
                      'https://www.madewell.com/cashmere-sweatshirt-K5037.html?color=OR0020']

class TestMadewell_Scrape(unittest.TestCase):

    def test_get_productDetails(self):
        self.assertEqual(get_productDetails(['https://www.madewell.com/baum-und-pferdgarten-maiko-puff-sleeve-top-AG932.html?color=EB4488']), [product_search_shirts[0]])
        self.assertEqual(get_productDetails(['https://www.madewell.com//baum-und-pferdgarten-aubree-tie-waist-shirt-AG933.html?color=EB4489']), [product_search_shirts[1]])


    def test_search_product(self):
        self.assertEqual(search_product(item_name='sweater')[:7], search_result_list)



    def test_navigate_product(self):
        self.assertEqual(navigate_product()[:3], product_nav_list)