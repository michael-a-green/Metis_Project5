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
    prediction_matched = False
    session["prediction_performed"] = False
    y_pred = 0
    y_test = 0
    
    
    if review_form.validate_on_submit():

        #check that the exact same review text isn't being added twice
        review = ReviewTable.query.filter_by(review=review_form.review.data).first()


        if review is None:

            #This review has never been seen before so perform a prediction on it
            userinput_dict = {"review_text" : [review_form.review.data], "review_title" : [review_form.review_title.data], "review_star_rating" : [review_form.user_rating.data] }
            userinput_df = pd.DataFrame(userinput_dict)
            y_pred = clf.predict(userinput_df)
            y_test = userinput_df.review_star_rating.apply(clf.gen_net_promoter)
            y_test = y_test[0]
            session["prediction_performed"] = True
            
            #review never seen so add it to the database
            
            #create DB object from form data
            review_db_obj = ReviewTable(
                movie_title=review_form.movie_title.data,
                review_title=review_form.review_title.data,
                review=review_form.review.data,
                user_rating=review_form.user_rating.data,
                machine_rating=y_pred
            )
            
            if y_pred  == y_test:
                prediction_matched = True
            else:
                prediction_matched = False
            
                db.session.add(review_db_obj)
                db.session.commit()
                session["known"] = False
            return redirect(url_for(".index"))

        else:
            #review seen before
            session["known"] = True
        #return redirect( url_for(".index")  )
    
    return render_template("index.html",
                           current_time=datetime.utcnow(),
                           known=session.get("known",False),
                           prediction_performed=session.get("prediction_performed",False),
                           review_form=review_form,
                           prediction_matched=prediction_matched)
