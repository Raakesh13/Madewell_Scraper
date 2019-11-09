import os
from bs4 import BeautifulSoup
from selenium import webdriver
import shutil
import requests

base_url = 'https://www.mi.com/in/'
mobile_list_url = base_url+'/list/'
driver = webdriver.Chrome('/home/rakesh/Drivers/chromedriver_linux64/chromedriver')
driver.get(mobile_list_url)
html = driver.execute_script('return document.documentElement.outerHTML')
mobile_list_soup = BeautifulSoup(html, 'html.parser')
mobile_list = mobile_list_soup.find_all('div', {'id': '1'})
mobile_name_list = list()
mobile_name_list = mobile_list[0].find_all('href')
# for i in range(22):
#     mobile_name_list.append(mobile_list[0].find_all('href')[i])
href = mobile_list[0].find_all('a')
href_list = list()
for j in href:
    if j['href'] not in href_list:
        href_list.append(j['href'])
print(href_list)
# for i in range(len(mobile_name_list)):
#     mobile_name_list[i] = mobile_name_list[i].replace(' ', '-')
# base_dir = os.getcwd()
# for i in mobile_name_list:
#     print(base_url+i)
#     driver.get(base_url+i)
#     html = driver.execute_script('return document.documentElement.outerHTML')
#     img_soup = BeautifulSoup(html, 'html.parser')
#     image = []
#     for j in img_soup.find_all('img'):
#         print(j)
#         try:
#             src = j['src']
#         except:
#             pass
#         if src[-3:] == 'jpg' or src[-3:] == 'png':
#             image.append(src)
#         print(image)
#     current_dir = os.path.join(base_dir, i)
#     if not os.path.exists(current_dir):
#         os.makedirs(current_dir)
#     os.chdir(current_dir)
#     current_dir = os.getcwd()
#     for img in image:
#         filename = os.path.basename(img)
#         img_r = requests.get(img, stream=True)
#         new_path = os.path.join(current_dir, filename)
#         with open(new_path, 'wb') as outputfile:
#             shutil.copyfileobj(img_r.raw, outputfile)
#         del(img_r)






driver.quit()
