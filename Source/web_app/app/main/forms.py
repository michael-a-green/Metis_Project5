"""
Forms go in here
Essentially objects that capture user input

"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length,NumberRange, AnyOf, InputRequired

#This is the form that will get populated by the user of the
#web application
class ReviewForm(FlaskForm):
    """
    schema
    movie_title|review_title |review text             |user_rating|machine_rating
    -----------|-------------|------------------------|-----------|-----------|--------------
    The Blob   |It was great!|I saw it. It was great!.|10         |10         |

    """
    movie_title = StringField("What is the title of the movie?", validators=[DataRequired(),Length(min=1, max=500)])
    review_title = StringField("What is the title for your review?", validators=[DataRequired(),Length(min=1, max=500)])
    #review = StringField("What is your review for the movie??", validators=[DataRequired(),Length(min=1, max=1000)])
    review = TextAreaField("What did you think of the movie?", validators=[DataRequired(), Length(min=1, max=5000)])
    user_rating = IntegerField("What is the rating you give for this movie? Please provide a rating between 1 (one of the worst) and 10 (one of the best)", validators=[InputRequired(),NumberRange(min=1,max=10)])
    #movie_rating = IntegerField("what is the traing you give for this movie? Pleae provide a rating 1 0", validators=[InputRequired(),NumberRange(min=1,max=10)])    

    submit = SubmitField("Submit")
    
    
