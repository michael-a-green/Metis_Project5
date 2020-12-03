"""
sql alchemy db object go in here
object that represents the underlying SQL database

"""

from . import db

class ReviewTable(db.Model):
    __tablename__ = "review_table"
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(500))
    review_title = db.Column(db.String(500))
    review = db.Column(db.String(5000))
    user_rating = db.Column(db.Integer)
    machine_rating = db.Column(db.Integer)

    def __repr__(self):
        return "movie_title = %r\nreview_title = %r\nreview => \n%r\nuser_rating = %0d\machine_rating = %0d\n"%(self.movie_title, self.review_title, self.review, self.user_rating, self.machine_rating)
    
    
