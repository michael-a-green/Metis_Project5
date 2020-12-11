from datetime import datetime
import pandas as pd
import numpy as np
from flask import render_template, session, redirect, url_for
from . import main
from .forms import ReviewForm
from .. import db
from ..models import ReviewTable
from ..predictor import MyClassifier


clf = MyClassifier()


    
@main.route('/', methods=["GET", "POST"])
def index():
    review_form = ReviewForm()

    #what the model will predict
    #hardcoded for now
    #TODO Incorp the model prediction
    MACHINE_RATING = 10
    #prediction_matched = False
    #session["prediction_performed"] = False
    #y_pred = 0
    #y_test = 0
    
    
    if review_form.validate_on_submit():

        #check that the exact same review text isn't being added twice
        review = ReviewTable.query.filter_by(review=review_form.review.data).first()
        print("Received a form")


        if review is None:

            #This review has never been seen before so perform a prediction on it
            print("Never saw this review so going to do a predict on it")            
            userinput_dict = {"review_text" : [review_form.review.data], "review_title" : [review_form.review_title.data], "review_star_rating" : [review_form.user_rating.data] }
            userinput_df = pd.DataFrame(userinput_dict)
            y_pred = clf.predict(userinput_df)
            y_test = userinput_df.review_star_rating.apply(clf.gen_net_promoter)
            y_test = y_test[0]

            print("Did prediction. y_pred = {} y_test = {}".format(y_pred, y_test))

            #converting y_pred to a python int
            y_pred = int(y_pred)
            y_test = int(y_test)
            print("After conversion. y_pred = {} y_test = {}".format(y_pred, y_test))
            
            session["prediction_performed"] = True            
            session["y_pred"] = y_pred
            session["y_test"] = y_test
            
            #review never seen so add it to the database
            
            #create DB object from form data
            review_db_obj = ReviewTable(
                movie_title=review_form.movie_title.data,
                review_title=review_form.review_title.data,
                review=review_form.review.data,
                user_rating=review_form.user_rating.data,
                machine_rating=y_pred
            )
            print("Created data base object =>\n{}n".format(review_db_obj))
            
            if session.get("y_pred", 0) == session.get("y_test", 0):
                session["prediction_matched"] = True
            else:
                session["prediction_matched"] = False
            
            db.session.add(review_db_obj)
            db.session.commit()
            print("Finished writing into database")
            session["known"] = False
            #print("Doing redirect url")            
            #return redirect(url_for(".index"))

        else:
            #review seen before
            print("Found in database already!")
            session["known"] = True
            session["prediction_performed"] = False            
            
        print("Doing redirect url")                        
        return redirect( url_for(".index")  )

    print("type(y_pred) = {} y_pred = {}".format(type( session.get("y_pred", 0)), session.get("y_pred", 0)))
    print("type(y_test) = {} y_test = {}".format(type( session.get("y_test", 0)), session.get("y_test", 0)))
    print("just before render: prediction_performed = {}".format(session.get("prediction_performed",False)))

    return render_template("index.html",
                           current_time=datetime.utcnow(),
                           known=session.get("known",False),
                           prediction_performed=session.get("prediction_performed",False),
                           review_form=review_form,
                           prediction_matched=session.get("prediction_matched",False), y_test=session.get("y_test", 0), y_pred=session.get("y_pred", 0))
