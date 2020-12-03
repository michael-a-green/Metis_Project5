from flask import Blueprint

main = Blueprint("main", __name__)



#please make sure this line is the last non-blank line in the file
from . import views, errors
