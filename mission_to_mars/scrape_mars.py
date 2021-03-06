# import
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt


# set up driver
# executable_path = {'executable_path': '/Applications/chromedriver'}
# browser = Browser('chrome', **executable_path, headless = False)

##########
#Mars News
##########

def mars_news(browser):

  # visit site on driver
  url = 'https://mars.nasa.gov/news/'
  browser.visit(url)


  # get first list & wait .5
  browser.is_element_not_present_by_css('ul.item_list li.slide', wait_time = 0.5)
  
  # parse with bs4
  html = browser.html
  news_soup = BeautifulSoup(html, 'html.parser')

  try:
      # show/test
      slide_element = news_soup.select_one('ul.item_list li.slide')
      slide_element.find('div', class_ = 'content_title')

      # scrape newest titles
      news_t = slide_element.find('div', class_ = 'content_title').get_text()
      news_p = slide_element.find('div', class_ = 'article_teaser_body').get_text()
  except AttributeError:
    return None, None
  return news_t, news_p

################
#JPL Mars Images
################

def featured_image_url(browser):

  #Visit Base URL
  url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
  browser.visit(url)

  #Nav to Img
  browser.find_by_css('.BaseImagePlaceholder.dark-theme').first.click()
  browser.find_by_css('.PageImageDetail aside .BaseButton').first.click()

  #Pull url
  html = browser.html
  image_soup = BeautifulSoup(html, 'html.parser')

  try:
      featured_image_url = image_soup.select_one('img').get('src')
  except AttributeError:
    return None
  return featured_image_url

###########
#Mars Facts
###########

def mars_facts():

  #Visit Base URL & Pull Table
  try:
    mars_facts_df = pd.read_html('https://space-facts.com/mars/')[0]
  except BaseException:
    return None
  mars_facts_df.columns = ['Description', 'Value']

    #Convert to HTML
  return mars_facts_df.to_html(index = False)

#################
#Mars Hemispheres
#################

def hemisphere(browser):

#Vist Base URL
  url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
  browser.visit(url)

  #List to append
  hemisphere_image_urls = []

  #For Loop for all URLs
  links = browser.find_by_css('a.product-item h3')
  for i in range(len(links)):
      hemisphere = {}
      browser.find_by_css('a.product-item h3')[i].click()
      sample_element = browser.find_link_by_text('Sample').first
      hemisphere['img_url'] = sample_element['href']
      hemisphere['title'] = browser.find_by_css('h2.title').text
      hemisphere_image_urls.append(hemisphere)
      browser.back()
  return hemisphere_image_urls

######################
#Main Web Scraping Bot
######################

def scrape_all():

  executable_path = {'executable_path': '/Applications/chromedriver'}
  browser = Browser('chrome', **executable_path, headless = False)
  news_t, news_p = mars_news(browser)
  img_url = featured_image_url(browser)
  facts = mars_facts()
  hemisphere_image_urls = hemisphere(browser)
  timestamp = dt.datetime.now()

  data = {
    'news_t': news_t,
    'news_p': news_p,
    'featured_image': img_url,
    'facts': facts,
    'hemisphere': hemisphere_image_urls,
    'last_modified': timestamp
  }
  browser.quit()
  return data

if __name__ == '__main__':
  print(scrape_all())