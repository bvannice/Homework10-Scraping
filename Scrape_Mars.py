from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd 
from time import sleep

#mars news scrape

def scrape():
    marsScrape = {}

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    while not browser.is_element_present_by_tag("li", wait_time=5):
        pass

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text

    marsScrape["news_title"] = news_title
    marsScrape["news_p"] = news_p

    #featured image url scrape
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_base = "https://www.jpl.nasa.gov"
    feature_image = soup.find("div", class_="carousel_items").find("article")["style"]
    featured_image_url = feature_image.split("'")[1]
    featured_image_url = featured_base + featured_image_url

    marsScrape["featured_image_url"] = featured_image_url

    #WeatherTweets
    weather_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_twitter)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweets = soup.find('div', class_="stream").find('ol').find_all('li', class_="js-stream-item")
    for tweet in tweets:
        tweet_text = tweet.find('div', class_="js-tweet-text-container").text
        if "Sol " in tweet_text:
            mars_weather = tweet_text.strip()
            break


#mars facts
    marsFacts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(marsFacts_url)

    marsFacts_df = tables[0]
    marsFacts_df.columns = ["Description", "Value"]
    marsFacts_df = marsFacts_df.set_index("Description")

    html_table = marsFacts_df.to_html()
    html_table = html_table.replace('\n', '')
