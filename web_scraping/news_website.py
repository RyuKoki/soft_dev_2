# news_website.py

# reference how to web scraping 
# # https://medium.com/equinox-blog/%E0%B8%A5%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B3-web-scraping-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-beautifulsoup-%E0%B8%81%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%96%E0%B8%AD%E0%B8%B0-b58dc0e1775a

# Thank you "BBC News website"
# https://www.bbc.com/news

###############################################################
# You have to install 'bs4' for using 'BeautifulSoup'
# # First way [by command line]
# # # 1. Open 'cmd' of window
# # # 2. Type 'pip install beautifulsoup4'
# # Second way [by terminal in VS Code]
# # # Type 'python -m pip install beautifulsoup4'
###############################################################

import requests
from bs4 import BeautifulSoup

# download centents in website
web_data = requests.get("https://www.bbc.com/news")
# print(web_data) 
# # <Response [200]> means request success
# # <Response [4xx]> or [5xx] means error

# test to print html code on website but disorder style
# print(web_data.content)

soup = BeautifulSoup(web_data.text, 'html.parser')
# test to print html code on website but html style
# print(soup)

# find all of contents by TAG html
# i.e. <p>, <a ...>, <li...>, <span...>, etc...
# You can find it by 2 ways
# # 1. Control mouse pointer at the content and a right click 'Inspect'
# # 2. Press 'F12' at your keyboard
# print(soup.find_all('span')[20].getText())

# find all of contents by id or class html
# This is 'Most read' in https://www.bbc.com/news
# You can find the name of class by choosing 
# # 'Select an element in the page to inspect it'
# # and you'll see mouse pointer and click the heading 
# # which you want to get them all!

###############################################################
########################Most Read News#########################

most_read = soup.find_all('a', href=True,  
        class_="gs-c-promo-heading nw-o-link gs-o-bullet__text gs-o-faux-block-link__overlay-link gel-pica-bold gs-u-pl-@xs", )
# show the 'Most read' heading on website
print('Most Read')
print('--------------------------------------------------')
for heading_r in range(len(most_read)):
    # getting header NAMEs
    header_name_r = most_read[heading_r].getText()
    print(heading_r+1, header_name_r)
    # getting link of each of headers
    header_link_r = most_read[heading_r]['href']
    print("\thttps://www.bbc.com" + header_link_r)

###############################################################



###############################################################
#######################Most Watched News#######################

most_watched = soup.find_all('a', href=True, 
        class_='gs-c-promo-heading nw-o-link gs-o-bullet__text gs-o-faux-block-link__overlay-link gel-pica-bold gs-u-pl@xs')
# show the 'Most Watched' heading on website
print('Most Watched')
print('--------------------------------------------------')
for heading_w in range(len(most_watched)):
    # getting header NAMEs
    header_name_w = most_watched[heading_w].getText()
    print(heading_w+1, header_name_w.strip("Video"))
    # getting link of each of headers
    header_link_w = most_watched[heading_w]['href']
    print("\thttps://www.bbc.com" + header_link_w)

###############################################################



