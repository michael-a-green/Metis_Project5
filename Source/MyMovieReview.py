"""

Module MyMovie Review

Contains the definition for the class MoviewReview

"""

import os
import re
import time
from random import randint

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

from project5_utils import my_print
from project5_utils import my_wait



class MovieReview:
    """

    Class that represents a single movie review
    It inherits from class Movie so has all of it's features

    In addition to those, it contains the following
    review_text: Full text review for the movie represented by its other features
    review_star_rating: The integer star rating (out of 10). This will represent a categorical label for the review
    
    

    """

    ############################################
    ###
    ### Constructor
    ###
    ############################################
    def __init__(self,
                 title,
                 reviewlink_url,
                 directlink_url,
                 review_text="EMPTY",
                 review_star_rating=-1,
                 reviewer_name="DEFAULT_NAME",
                 review_title="EMPTY",
                 review_date="EMPTY"):


        self.review_text = review_text
        self.review_star_rating = review_star_rating
        self.reviewer_name = reviewer_name
        self.directlink_url = directlink_url
        self.reviewlink_url = reviewlink_url

        #movie title
        self.title = title
        #title reviewer gave for the reviewer's review
        self.review_title = review_title
        self.review_date = review_date

        

    def __repr__(self):
        temp_string = "movie title = {}\nreview_url = {}\nreview_text = \n{}\nreview_star_rating = {}\n\
reviewer_name = {}\nmovie URL = {}\nreview_title = {}\nreview date = {}\n".format(self.title,
                                                                                  self.reviewlink_url,
                                                                                  self.review_text,
                                                                                  self.review_star_rating,
                                                                                  self.reviewer_name,
                                                                                  self.directlink_url,
                                                                                  self.review_title,
                                                                                  self.review_date)
        return temp_string
    
        

class MovieReviewGenerator:
    """
    This class takes a URL to a movie on IMDB
    and generates objects of the class MovieReview
    for that movie.
    """
    ############################################
    ###
    ### Constructor
    ###
    ############################################
    def __init__(self, title, movie_url):
        
        #title of the movie
        self.title = title
        
        #IMDB URL to the movie page
        self.movie_url = movie_url

        #Link to the IMDB page that lists reviews to the
        #movie located at movie_url
        self.reviews_url = ""

        self.IMDB_ROOT = "http://www.imdb.com"

        #list of URL's to movie reviews
        self.review_urls = []

        #properties used to launch chrome browser that'll be controlled by this
        #review generator through selenium
        self.chrome_options = Options()
        ##needed to run on the linux machine used to test this code
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")        
        
        self.chrome_driver = "/opt/google/chrome/chromedriver"
        
    def collect_review_urls(self, numb_reviews=-1, start_time=10, stop_time=20, DEBUG=0, LOG_FILE=None):
        """

        This function uses movie_url to then find the
        URL to the reviews for the movie (called, review_url)

        It then finds the links to numb_reviews reviews for that movie. If numb_reviews=-1, then it finds all of them

        It stores these URLs in review_urls.

        
        """
        
        my_print("waiting before accessing {} for movie {}".format(self.movie_url, self.title), DEBUG, LOG_FILE)
        my_wait(start_time,stop_time)
        
        temp_web_response = requests.get(self.movie_url)
        
        #did the scrape succeed?
        if temp_web_response.status_code != 200:
            my_print("error: Could not get web page for movie = {}".format(self.title), 1, LOG_FILE)
            return
        
        temp_web_response_text = temp_web_response.text
        temp_web_soup = BeautifulSoup(temp_web_response_text, features="lxml")

        #get all <a> where id="quicklink"
        #hoping to get this
        #
        #
        # <a href="<URL>" class="quicklink">USER REVIEWS</a>
        #
        #
        #
        #
        listofQuickLinkA = temp_web_soup.find_all("a", class_="quicklink")

        ###################################
        #
        # Searching for URL to user reviews
        #
        ###################################

        for quickLinkA in listofQuickLinkA:
            
            if quickLinkA.text == "USER REVIEWS":
                self.reviews_url = self.IMDB_ROOT + quickLinkA.get("href")
                my_print("link to reviews for movie {} is {}".format(self.title, self.reviews_url), DEBUG, LOG_FILE)
                break

        ##navigate to reviews, collect numb_reviews
        if not self.reviews_url:
            my_print("Error. Not reviews found for movie {} at URL {} ".format(self.title, self.movie_url),1,LOG_FILE)
            return
        #we likely found a reviews URL for this movie
        else:
            #collect movie URLs
            my_wait(start_time, stop_time)
            reviews_web_response = requests.get(self.reviews_url)

            if reviews_web_response.status_code != 200:
                my_print("Error: web request for reviews on movie {} failed! Review URL is {}".format(self.title, self.reviews_url),1,LOG_FILE)
                return
            
            reviews_web_response_text = reviews_web_response.text
            reviews_web_soup = BeautifulSoup(reviews_web_response_text, features="lxml")

            ###################################
            #
            # Decide number of reviews to pull
            #
            ###################################
            if numb_reviews <= 0 :
                #get them all
                headerDIV = reviews_web_soup.find("div", class_="header")
                
                # big assumption: There is only one <div class="header"> on this page
                headDivSpan = headerDIV.find("span")
                headDivSpan_text = headDivSpan.text
                temp_numb_reviews, _ = headDivSpan_text.split()
                temp_numb_reviews = temp_numb_reviews.replace(",","")
                temp_numb_reviews = int(temp_numb_reviews)

            else:
                temp_numb_reviews = numb_reviews

            #get review a_tags:
            temp_driver = webdriver.Chrome(self.chrome_driver, options = self.chrome_options)
            temp_old_number_of_reviews = 0
            temp_driver.get(self.reviews_url)

            while(temp_numb_reviews > 0):
            
                listofTitleA = reviews_web_soup.find_all("a", class_="title")
                temp_list_of_review_urls = [ titleA.get("href") for titleA in listofTitleA  ]
                self.review_urls = self.review_urls + temp_list_of_review_urls
                self.review_urls = set(self.review_urls)
                self.review_urls = list(self.review_urls)
                temp_current_number_reviews = len(self.review_urls)

                temp_numb_reviews -= (temp_current_number_reviews - temp_old_number_of_reviews)
                temp_old_number_of_reviews = temp_current_number_reviews

                #download the next set of reviews
                #need to click a button so using selenium

                my_wait(start_time,stop_time)
                
                try:
                    get_more_button = temp_driver.find_element_by_xpath("//*[contains(text(), 'Load More')]")
                    get_more_button.click()
                except NoSuchElementException:
                    my_print("No \"Load More\" Button. You're done scraping this movie.", DEBUG, LOG_FILE)
                    break
                except ElementNotInteractableException:
                    my_print("Could not find \"Load More\" Button. You're done scraping this movie.", DEBUG, LOG_FILE)
                    break
                    
                
                my_wait(start_time,stop_time)

                #get the HTML for this and parse it into a soup object
                reviews_web_soup = BeautifulSoup(temp_driver.page_source, features="lxml")
            
            temp_driver.close()
            
            if len(self.review_urls) > numb_reviews:
                self.review_urls = self.review_urls[:numb_reviews]
            
        


    def generate_review(self, start_time=10, stop_time=20, DEBUG=0, LOG_FILE=None):
        """
        Generates a single review from a list of reviews as a MovieReview Object
        
        """

        if len(self.review_urls) == 0:
            my_print("Error: this generator does not have a list of reviews!", 1, LOG_FILE)
            return

        for temp_review_url in self.review_urls:

            #request page
            my_wait(start_time, stop_time)
            temp_request_review_url = self.IMDB_ROOT + temp_review_url
            temp_review_web_response = requests.get(temp_request_review_url)

            if temp_review_web_response.status_code != 200:
                my_print("Error: Web request for review URL {} failed for movie {}".format(temp_request_review_url, self.title), 1, LOG_FILE)
                #not returning just going to the next one
                continue

            #convert it to a soup object
            temp_review_web_response_text  = temp_review_web_response.text
            temp_review_web_soup = BeautifulSoup(temp_review_web_response_text, features="lxml")

            ##
            ##
            ## Need to pull the following
            ##
            ## title of the review
            ## review text (if not present skip)
            ## star rating for the review (if not present skip)
            ## username of the reviewer
            ## review date
            ##
            ##


            """

            title of review:

            <a href=... class="title">REVIEW TITLE</a>

            review text:

            <div class="text show-more__control">REVIEW TEXT</div>

            star rating:

            <span class="rating-other-user-rating">
               ...
               <span>STAR RATING</span>
               ...
            </span>

            reviewer username:

            <div class="parent">
              <h3>
                <a href=STUFF>REVIEWER USERNAME</a>
              </h3>
            </div>

            review date:
            
            <span class="review-date">DATE I WANT</span>
            

            """

            #there's only 1
            titleA = temp_review_web_soup.find("a", class_="title")
            temp_review_title = titleA.text
            temp_review_title = temp_review_title.rstrip()
            temp_review_title = temp_review_title.lstrip()

            textDIV = temp_review_web_soup.find("div", class_="text")
            temp_review_text = textDIV.text

            userRatingSpan = temp_review_web_soup.find("span", class_="rating-other-user-rating")

            #assumption: The first span has the info I want
            if userRatingSpan == None:
                temp_review_rating = 0
            else:
                ratingSpan = userRatingSpan.find("span")
                temp_review_rating = ratingSpan.text
                temp_review_rating = int(temp_review_rating)

            parentDIV = temp_review_web_soup.find("div", class_="parent")
            usernameA = parentDIV.find("a")
            temp_user_name = usernameA.text

            reviewDateSpan = temp_review_web_soup.find("span", class_="review-date")
            temp_review_date = reviewDateSpan.text

            if temp_review_text and temp_review_rating:
                temp_movie_review = MovieReview(title=self.title,
                                                 reviewlink_url=temp_request_review_url,
                                                 directlink_url=self.movie_url,
                                                 review_text=temp_review_text,
                                                 review_star_rating=temp_review_rating,
                                                 reviewer_name=temp_user_name,
                                                 review_title=temp_review_title,
                                                 review_date=temp_review_date)
                my_print("created moview review =>\n{}\n".format(temp_movie_review), DEBUG, LOG_FILE)
                yield temp_movie_review
            
            else:
                my_print("review at URL {} for movie {} didn't have text and a rating".format(temp_request_review_url, self.title))
            
            
        
    
        

    
