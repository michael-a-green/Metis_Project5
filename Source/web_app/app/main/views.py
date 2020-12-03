from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import ReviewForm
from .. import db
from ..models import ReviewTable


@main.route('/', methods=["GET", "POST"])
def index():
    review_form = ReviewForm()

    #what the model will predict
    #hardcoded for now
    #TODO Incorp the model prediction
    MACHINE_RATING = 10
    prediction_matched = False

    
    if review_form.validate_on_submit():

        #check that the exact same review text isn't being added twice
        review = ReviewTable.query.filter_by(review=review_form.review.data).first()

        if review is None:
            
            #review never seen so add it to the database
            
            #create DB object from form data
            review_db_obj = ReviewTable(
                movie_title=review_form.movie_title.data,
                review_title=review_form.review_title.data,
                review=review_form.review.data,
                user_rating=review_form.user_rating.data,
                machine_rating=MACHINE_RATING
            )
            
            if review_form.user_rating.data  == MACHINE_RATING:
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

    return render_template("index.html", current_time=datetime.utcnow(), known=session.get("known",False), review_form=review_form, prediction_matched=prediction_matched)
