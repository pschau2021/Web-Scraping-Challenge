##########################################################################
# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
##########################################################################
# Set the chromedriver path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser ('chrome', **executable_path, headless=True)
##########################################################################
  
def scrape():
    scraped_data = {}
    news_data_output = mars_news()
    scraped_data["mars_news"] = news_data_output[0]
    scraped_data["mars_paragraph"] = news_data_output[1]
    scraped_data["mars_image"] = mars_image()
    scraped_data["mars_facts"] = mars_facts()
    scraped_data["mars_hemisphere"] = mars_hemis_data()
    browser.quit()
    return scraped_data
    
#########################################################################
# NASA Mars News
#########################################################################
# Scrape the Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
def mars_news():    
    url = "https://redplanetscience.com/"
    browser.visit(url)
    # Create BeautifulSoup object; parse with 'html.parser
    html = browser.html
    soup = bs(html, "html.parser")

# Get the title and content text in the latest news
    news_title = soup.find('div', class_ ='content_title')[0].text
    print(f"News Title: {news_title}")
    
    news_p = soup.find('div', class_ ='article_teaser_body')[0].text
    print(f"News Paragraph: {news_p}")
    news_data_output = [news_title, news_p]
    return news_data_output

########################################################################
# JPL Mars Space Images - Featured Image
########################################################################
# Visit the following URL
def mars_image():
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

# Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
# Assign the url string to a variable called featured_image_url.
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://spaceimages-mars.com/" + image
    print(f"url: {featured_image_url}")
    return featured_image_url

#######################################################################
# Mars Facts
#######################################################################
# Use Pandas to scrape the table containing facts about the planet
def mars_facts():
    url = 'https://galaxyfacts-mars.com/'
    tables_facts = pd.read_html(url)
    tables_facts

# Convert data to dataframe
    facts_df = tables_facts[0]
    facts_df.columns = ['Description', 'Mars', 'Earth']
    facts_df

# Convert the data to a HTML table string
    html = facts_df.to_html()
    return html

######################################################################
# Mars Hemispheres
######################################################################
# Visit Mars Hemispheres url to obtain high resolution images for each of Mar's hemispheres.

# Set the chromedriver path
def mars_hemis_data():
    hemis_url = "https://marshemispheres.com/"
    browser.visit(hemis_url)

# Collect the urls by clicking each of the links to the hemispheres
# Retrieve the titles and urls and append to list
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_list = []
    category = soup.find("div", class_ = "result-list" )
    hemispheres =category.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        title = title.strip("Enhanced")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link   
        browser.visit(image_link)
        hemisphere_html = browser.html
        soup = bs(hemisphere_html, 'html.parser')
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_list.append({"title": title, "img_url": image_url})
    return hemisphere_list  


