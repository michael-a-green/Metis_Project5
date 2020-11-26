"""

module mymovie

contains definition for class Movie

You must do the following imports before using this module

"""
from bs4 import BeautifulSoup
import requests
import re
import time
from random import randint

import pickle
from MyMovieReview import MovieReview
from MyMovieReview import MovieReviewGenerator

class Movie:
    """
    Class to represent the movies

    TODO: describe data members

    TODO: describe methods

    """

    #######################################
    #
    # Constructor
    #
    #######################################
    def __init__(self,title,directlink_url):

        self.title = title

        #directlink_url is the URL you would use to 
        #navigate to the page for the movie in IMDB
        self.directlink_url = directlink_url

        #these data members will
        #be set by another method called TODO: write name here
        self.domesticTotalGross = 0
        self.rating = ""
        self.director = ""
        self.releaseDate = ""
        self.genre = ""
        self.runtime = 0
        self.cast1 = ""
        self.cast2 = ""
        self.cast3 = ""
        self.budget = 0
        self.star_rating  = 0

    #######################################
    #
    # print overload operator
    #
    #######################################
    def __repr__(self):
        temp_string = "title = {} domesticTotalGross = {}\
 rating = {} director = {} releaseDate = {} runtime = {}\
 cast1 = {} cast2 = {} cast3 = {}  genre = {} budget = {} star_rating = {} directlink_url = {}".format(self.title,
                                                    self.domesticTotalGross,
                                                    self.rating,
                                                    self.director,
                                                    self.releaseDate,
                                                    self.runtime,
                                                    self.cast1,
                                                    self.cast2,
                                                    self.cast3,
                                                    self.genre,
                                                    self.budget,
                                                    self.star_rating,
                                                    self.directlink_url)
        return temp_string

    #######################################
    #
    # populate_movie()
    #
    #######################################
    def populate_movie(self,start_time=10,stop_time=20,DEBUG=0,LOG_FILE=None):
        """
		This method will use directlink_url to make a request for the page at that link
        It will then search through that link and find the information

        To facilitate running this in a comprehension it will before returning
        wait a random amount of time


        TODO: Swap out domesticTotalGross for genre
        TODO: Collect stars 
        TODO: Get the name of 1-3 actors
      
		"""
        temp_web_response = None
        temp_wait_time = None
        
        if start_time <= 0:
            start_time = 10
            
        if stop_time <= 0:
            stop_time = 20
        
        if stop_time <= start_time:
            stop_time = start_time + 10
        

        temp_wait_time = randint(start_time,stop_time)
        
        if DEBUG:
            print("movie {} waiting for {}".format(self.title, temp_wait_time),file=LOG_FILE)
        time.sleep(temp_wait_time)

        temp_web_response = requests.get(self.directlink_url)

        #did the scrape succeed?
        if temp_web_response.status_code != 200:
            print("error: Could not get web page for movie = {}".format(self.title),file=LOG_FILE)
            return

        #OK You got the scrape back, continue

        #searching for the data members of this Movie
        temp_web_response_text = temp_web_response.text
        temp_web_response_soup = BeautifulSoup(temp_web_response_text, features="lxml")

        #get all of the <div class="txt-block"> tags off this page
        listOfIDTxtBlockDIV = temp_web_response_soup.find_all("div", class_="txt-block")

        ################################################################################
        #The data I need lives inside these <div> tags
        #so search them one by one to find it
        #TODO: If you need to speed up your code maybe this is a place to start working
        #
        #In this for loop looking for the following values
        #
        # * MPAA rating
        # * Release Date
        # * Budget
        # * Domestic Gross
        # * Run time
        #
        ###############################################################################
        
        found_rating = 0
        found_releasedate = 0
        found_budget = 0
        found_domesticgross = 0
        found_runtime = 0
        
        for IDTxtBlockDV in listOfIDTxtBlockDIV:
        
            if found_rating and found_releasedate and found_budget and found_domesticgross and found_runtime:
                break
                
            IDTxtBlockDV_h4_tags = IDTxtBlockDV.find_all("h4")
            
            for h4_tags in IDTxtBlockDV_h4_tags:
            
                if re.match(r"Runtime",h4_tags.text):
                    
                    #get <time> tags
                    IDTxtBlockDV_time_tags =  IDTxtBlockDV.find_all("time")
                    
                    #the first one is what we want
                    self.runtime = IDTxtBlockDV_time_tags[0].text
                    #assumption: runtime is always given units "min"
                    self.runtime = self.runtime.replace("min","")
                    self.runtime = self.runtime.rstrip()
                    self.runtime = self.runtime.lstrip()
                    self.runtime = int(self.runtime)
                    found_runtime = 1
                    
            text_of_IDTxtBlockDV  = IDTxtBlockDV.text

            lines_of_IDTxtBlockDV = text_of_IDTxtBlockDV.split("\n")
		    
            #search line by line the text of this <div> tag

            temp_rating = "NULL"
		    
            #careful I assign multiple types to this variable
            temp_budget = "NULL"

            temp_release_date = "NULL"
            found_budget = 0

            temp_domesticTotalGross = "NULL"

            for my_line in lines_of_IDTxtBlockDV:

                #search for rating
                m = re.match(r"Rated\s+([A-Za-z\-0-9]+)\s+", my_line)
                if m and found_rating==0:
                    temp_rating = m.group(1)
                    #any changes needed?
                    #if so they go here
                    temp_rating = temp_rating.rstrip()
                    temp_rating = temp_rating.lstrip()
                    self.rating = temp_rating
                    found_rating = 1


                #search for Release Date
                m = re.match(r"Release Date\:\s+(\d+\s+\w+\s+\d+)", my_line)
                if m and found_releasedate == 0:
                    temp_release_date = m.group(1)
                    self.releaseDate = temp_release_date
                    self.releaseDate = self.releaseDate.rstrip()
                    self.releaseDate = self.releaseDate.lstrip()
                    found_releasedate = 1

                #search for budget
                m = re.match(r"Budget\:\s*\$(.+)", my_line)
                if m and found_budget==0:
                    temp_budget = m.group(1)
                    #it's a string I want it to be an integer
                    temp_budget = temp_budget.rstrip()
                    temp_budget = temp_budget.lstrip()

                    #got to remove the ',' characters
                    temp_budget = temp_budget.replace(',','')
                    self.budget = int(temp_budget)
                    found_budget = 1

                #searching for domesticTotalGross
                m = re.match(r"Gross USA\:\s*\$(.+)", my_line)
                if m and found_domesticgross == 0:
                    temp_domesticTotalGross = m.group(1)
                    temp_domesticTotalGross = temp_domesticTotalGross.rstrip()
                    temp_domesticTotalGross = temp_domesticTotalGross.lstrip()
                    temp_domesticTotalGross = temp_domesticTotalGross.replace(',','')
                    self.domesticTotalGross = int(temp_domesticTotalGross)
                    found_domesticgross = 1

                
        #The director and stars (names of people in cast1,cast2,cast3)
        #reside in the <div class="credit_summary"     
        
        listOfCreditSummaryItemDIV = temp_web_response_soup.find_all("div", class_="credit_summary_item")
        
        ################################################################################
        #The data I need lives inside these <div> tags
        #so search them one by one to find it
        #TODO: If you need to speed up your code maybe this is a place to start working
        #
        #In this for loop looking for
        # * Director Name
        # * First star actor name
        # * Second star actor name
        #
        ###############################################################################
        for CreditSummaryItemDIV in listOfCreditSummaryItemDIV:

            CreditSummaryItemDIV_a_tags = CreditSummaryItemDIV.find_all("a")
            CreditSummaryItemDIV_h4_tags = CreditSummaryItemDIV.find_all("h4")

            for h4_tag in CreditSummaryItemDIV_h4_tags:

                #searching for director name
                if re.match(r"Director", h4_tag.text):

                    #BIG ASSUMPTION
                    #THERE IS ONLY 1 <a> tag
                    #IF THE <h4> tag has text Director
                    self.director = CreditSummaryItemDIV_a_tags[0].text

                    #clean it up
                    self.director = self.director.rstrip()
                    self.director = self.director.lstrip()

                #Searching for movie star names
                if re.match(r"Stars", h4_tag.text):

                    #get the first three
                    i = 0
                    for a_tag in CreditSummaryItemDIV_a_tags:

                        if i == 3:
                            break
                        if i == 0:
                            self.cast1 = a_tag.text
                        if i == 1:
                            self.cast2 = a_tag.text
                        if i == 2:
                            self.cast3 = a_tag.text
                        
                        i += 1

        ##########################################################
        #
        # <div class="see-more inline canwrap"> contains the genre
        #
        # In this loop looking for the following parameter(s)
        #
        # * genre
        #
        ###########################################################
    
        listOfSeeMoreInlineCanWrapDIV = temp_web_response_soup.find_all("div", class_="see-more inline canwrap")
    
        for SeeMoreInlineCanWrapDIV in listOfSeeMoreInlineCanWrapDIV:
            SeeMoreInlineCanWrapDIV_h4_tags = SeeMoreInlineCanWrapDIV.find_all("h4")
            SeeMoreInlineCanWrapDIV_a_tags = SeeMoreInlineCanWrapDIV.find_all("a")
            
            for h4_tag in SeeMoreInlineCanWrapDIV_h4_tags:
        
                if re.match(r"Genre", h4_tag.text):
                    #Just use the first genre listed
                    self.genre = SeeMoreInlineCanWrapDIV_a_tags[0].text
                    self.genre = self.genre.rstrip()
                    self.genre = self.genre.lstrip()
            
        ##################################################################
        #
        # <div class="ratingValue"> has the rating number
        # in a span: <span itemprop="ratingValue">RATING_NUMBER</span>
        # 
        # Searching for start_rating. Assumption: There are no 0 star
        # movies, so if start_rating==0 that means this movie
        # never received a star rating.
        # 
        # Example: https://www.imdb.com/title/tt1774365/?ref_=nv_sr_srsg_3
        #
        ##################################################################
        
        listOfRatingValueDIV = temp_web_response_soup.find_all("div", class_="ratingValue")
        
        for RatingValueDIV in listOfRatingValueDIV:
            
            ratingValueSpan = RatingValueDIV.find("span", itemprop="ratingValue")
            self.star_rating = ratingValueSpan.text
            self.star_rating = self.star_rating.rstrip()
            self.star_rating = self.star_rating.lstrip()
            self.star_rating = float(self.star_rating)
            
        
##############################
#    
# test code
#
##############################
if __name__ == "__main__":

    TEST_DEBUG = 1
    looper = Movie("Looper","https://www.imdb.com/title/tt1276104/?ref_=fn_al_tt_1")
    star_wars_iv = Movie("Star Wars Episode IV","https://www.imdb.com/title/tt0076759/?ref_=nv_sr_srsg_0")

    print(looper)
    print(star_wars_iv)

    assert(looper.title == "Looper")
    assert(star_wars_iv.title == "Star Wars Episode IV")

    #test populating movies

    beautiful_creatures = Movie("Beautiful Creatures","https://www.imdb.com/title/tt1559547")

    beautiful_creatures.populate_movie(DEBUG=TEST_DEBUG)

    assert(beautiful_creatures.title =="Beautiful Creatures")
    assert(beautiful_creatures.director =="Richard LaGravenese")
    assert(beautiful_creatures.domesticTotalGross == 19452138)
    assert(beautiful_creatures.rating == "PG-13")
    assert(beautiful_creatures.releaseDate == "14 February 2013")
    assert(beautiful_creatures.cast1 == "Alice Englert")
    assert(beautiful_creatures.cast2 == "Viola Davis")
    assert(beautiful_creatures.cast3 == "Emma Thompson")
    assert(beautiful_creatures.star_rating == 6.1)
    assert(beautiful_creatures.runtime == 124)

    print(beautiful_creatures)

    wolf_of_wallstreet = Movie("The Wolf of Wall Street","https://www.imdb.com/title/tt0993846/")
    wolf_of_wallstreet.populate_movie(DEBUG=1)
    
    assert(wolf_of_wallstreet.runtime==180)

    print(wolf_of_wallstreet)

    #reading in a movie from pkl. create review generator. read in reviews
    wolfOfWallStreetReviewGen = MovieReviewGenerator(wolf_of_wallstreet.title,wolf_of_wallstreet.directlink_url)
    wolfOfWallStreetReviewGen.collect_review_urls(numb_reviews=10, start_time=5, stop_time=15, DEBUG=TEST_DEBUG)

    list_of_reviews = []

    for myreview in wolfOfWallStreetReviewGen.generate_review(start_time=5, stop_time=20, DEBUG=TEST_DEBUG):
        print(myreview)
        list_of_reviews.append(myreview)
    

    #test out reading in the pickle file and getting reviews that way
    EXPANDED_PICKLE_FILE=open("../Data/Movie_populated_objects_4000.pkl","rb")

    mymovie = pickle.load(EXPANDED_PICKLE_FILE)
    mymovieReviewGenerator = MovieReviewGenerator(mymovie.title, mymovie.directlink_url)
    mymovieReviewGenerator.collect_review_urls(numb_reviews=20, start_time=5, stop_time=9, DEBUG=TEST_DEBUG)

    for myreview in mymovieReviewGenerator.generate_review(start_time=5, stop_time=7, DEBUG=TEST_DEBUG):
        print(myreview)
        list_of_reviews.append(myreview)

    EXPANDED_PICKLE_FILE.close()
    print("\nIf the print out of the text above is correct, and this string is printed, you passed.\n")

	
	
