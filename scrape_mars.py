#!/usr/bin/env python
# coding: utf-8

# Dependencies
import requests as req
import lxml.html as lh
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
from splinter import Browser

executable_path = {"executable_path":"/Users/allison/Desktop/chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)

# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# Mars News
def marsNews():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"html.parser")
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    output = [news_title, news_p]
    return output


# Mars Featured Image 
def marsImage():
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    xpath = '//*[@id="fancybox-lock"]/div/div[1]/img'
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.find("img", class_="fancybox-image")['src']
    featured_image_url = "https://www.jpl.nasa.gov" + img_url
    return featured_image_url

# Mars Weather 
def marsWeather():
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return mars_weather


# Mars Facts 
def marsFacts():
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    mars_facts = table[1]
    mars_facts.set_index(0, inplace=True)
    mars_html = mars_facts.to_html()
    return mars_html

