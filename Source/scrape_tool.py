#!/usr/bin/env python

#scrapes movie data from imdb and saves to a pickle file
#scrapes reviews for each move and saves to another pickle file

import os
import re
import time
from random import randint
import pickle

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


from project5_utils import my_print
from project5_utils import my_wait

from MyMovieReview import MovieReview
from MyMovieReview import MovieReviewGenerator

from mymovie import Movie



if __name__ == "__main__":

    #for each movie
    #grab URLS for the reviews
    #save this into a pickle file
    #grab each review (text, user, etc)
    #save that into another pickle file

    #TODO make this command line options if you get time
    NUMBER_OF_REVIEWS_PER_MOVIE=25
    DEBUG=1
    START_TIME = 3
    STOP_TIME = 8
    SAVE_REVIEWS_THRESHOLD = 1000

    #if PICK_UP is a 1 it will find the movie named in LAST_MOVIE
    #in  POPULATED_MOVIES_PKL_FILE  and rescrape from there
    PICK_UP = 1
    MOVIE_TITLE = "Boyhood"
    
    #Note I don't use a parameter for number of movies
    #because I'm reusing a old PKL file that has 4000 movies
    #so I'm scraping reviews for each movie in that PKL file

    #files
    log_file_name = "../Data/scrape_tool.log"
    LOG_FILE = open(log_file_name,"w")

    if not LOG_FILE:
        my_print("ERROR: Failed to open {} for output".format(log_file_name), DEBUG, LOG_FILE)
        exit(1)

    populated_movie_file_name = "../Data/Movie_populated_objects_4000.pkl"
    POPULATED_MOVIES_PKL_FILE = open(populated_movie_file_name,"rb")

    review_generator_pkl_file_name = "../Data/Review_Generators.pkl"
    
    if PICK_UP:
        REVIEW_GENERATORS_PKL_FILE = open(review_generator_pkl_file_name,"ab")
    else:
        REVIEW_GENERATORS_PKL_FILE = open(review_generator_pkl_file_name,"wb")        

    reviews_file_name = "../Data/Reviews.pkl"
    if PICK_UP:
        REVIEWS_PKL_FILE = open(reviews_file_name, "ab")
    else:
        REVIEWS_PKL_FILE = open(reviews_file_name, "wb")


    if PICK_UP:
        #####################################
        #
        # search for movie called MOVIE_TITLE
        #
        #####################################
        while 1:
            try:
                temp_start_movie = pickle.load(POPULATED_MOVIES_PKL_FILE)

                if temp_start_movie.title == MOVIE_TITLE:
                    my_print("Found movie {} picking up from there".format(temp_start_movie.title), DEBUG, LOG_FILE)
                    break
            except EOFError:
                my_print("Error did not find movie with title {} in the populated PKL file! Please check that you actually have it.".format(MOVIE_TITLE), DEBUG, LOG_FILE)
                exit(1)

    #variables to init before going into while loop
    first_iteration = 1
    review_count = 0
    save_reviews_threshold = SAVE_REVIEWS_THRESHOLD
                
    while 1:
        #code to enable stoping the tool with a file
        if os.path.isfile("STOP_SCRAPPING.txt"):
            my_print("Saw file STOP_SCRAPPING.txt. So will stop scraping.", DEBUG, LOG_FILE)
            break

        try:
            if review_count > save_reviews_threshold:
                my_print("Reopening Movie Review Generator and Reviews PKL Files", DEBUG, LOG_FILE)
                REVIEWS_PKL_FILE = open(reviews_file_name, "ab")
                REVIEW_GENERATORS_PKL_FILE = open(review_generator_pkl_file_name,"ab")

                if not REVIEWS_PKL_FILE:
                    my_print("Failed to open {} for writing".format(reviews_file_name), DEBUG, LOG_FILE)
                    exit(1)
                    
                if not REVIEW_GENERATORS_PKL_FILE :
                    my_print("Failed to open {} for writing".format(review_generator_pkl_file_name), DEBUG, LOG_FILE)
                    exit(1)

                #increment threshold
                if SAVE_REVIEWS_THRESHOLD < NUMBER_OF_REVIEWS_PER_MOVIE:
                    save_reviews_threshold += NUMBER_OF_REVIEWS_PER_MOVIE
                else:
                    save_reviews_threshold += SAVE_REVIEWS_THRESHOLD
                    
                my_wait(1,2)

            if first_iteration and PICK_UP:
                tempmovie = temp_start_movie
                first_iteration = 0
            else:
                tempmovie = pickle.load(POPULATED_MOVIES_PKL_FILE)
                
            tempmovieReviewGenerator = MovieReviewGenerator(tempmovie.title, tempmovie.directlink_url)
            tempmovieReviewGenerator.collect_review_urls(numb_reviews=NUMBER_OF_REVIEWS_PER_MOVIE,
                                                        start_time=START_TIME,
                                                        stop_time=STOP_TIME,
                                                        DEBUG=DEBUG,
                                                        LOG_FILE=LOG_FILE)
            pickle.dump(tempmovieReviewGenerator, REVIEW_GENERATORS_PKL_FILE)

            for myreview in tempmovieReviewGenerator.generate_review(start_time=START_TIME,
                                                                    stop_time=STOP_TIME,
                                                                    DEBUG=DEBUG,
                                                                    LOG_FILE=LOG_FILE
            ):
                pickle.dump(myreview, REVIEWS_PKL_FILE)
                review_count += 1

            #on every SAVE_REVIEWS_THRESHOLD reviews close the file to save it
            if review_count > save_reviews_threshold:
                my_print("Scraped {} reviews. Saving Movie Review Generator and Reviews PKL Files".format(review_count),
                         DEBUG, LOG_FILE)
                REVIEWS_PKL_FILE.close()
                REVIEW_GENERATORS_PKL_FILE.close()
                my_wait(1,2)
                    
            my_print("Done scrapping movie {}!".format(tempmovie.title), DEBUG, LOG_FILE)
            my_print("{} Reviews scraped".format(review_count), DEBUG, LOG_FILE)

        except EOFError:
            my_print("got EOF Exception", DEBUG, LOG_FILE)
            break


    my_print("Done scraping all movies", DEBUG, LOG_FILE)
    REVIEWS_PKL_FILE.close()
    REVIEW_GENERATORS_PKL_FILE.close()
    POPULATED_MOVIES_PKL_FILE.close()
        
    my_print("DONE", DEBUG, LOG_FILE)
    
