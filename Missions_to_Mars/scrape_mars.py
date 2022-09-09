from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', headless=False, **executable_path)

    # mars news
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    site = BeautifulSoup(html, 'html.parser')

    title = site.find('div', class_='content_title').get_text()
    parag = site.find('div', class_='article_teaser_body').get_text()

    # mars image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(1)

    browser.find_by_tag('button')[1].click()
    html = browser.html
    site = BeautifulSoup(html, 'html.parser')
    image_link = site.find('img', class_='headerimage fade-in').get('src')
    featured_image_url = url + image_link

    # mars facts
    url = 'https://galaxyfacts-mars.com'
    df = pd.read_html(url)
    mars_df = df[1]
    mars_df.columns=['Description','Mars']
    mars_fact_html = mars_df.to_html()

    # mars hemisphere
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    site = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []

    mars_pics = site.find_all('div', class_='description')

    for i in mars_pics:
            hemi = i.h3.text
            mars_img_link = i.a['href']
            img_url = url + mars_img_link
            mars_img_dict = {
                    'title' : hemi,
                    'img_url' : img_url
            }
            hemisphere_image_urls.append(mars_img_dict)
    hemisphere_image_urls

    browser.quit()

    mars = {
        "news_title": title,
        "news_paragraph": parag,
        "featured_image": featured_image_url,
        "mars_facts": mars_fact_html,
        "hemispheres_image": hemisphere_image_urls
    }

    return(mars)