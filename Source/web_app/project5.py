import os

import click

from app import create_app, db
from app.models import ReviewTable
from flask_migrate import Migrate

#env variable FLASK_CONFIG should be set to development, testing, production, or default
app = create_app(os.getenv("PROJECT5_CONFIG","default"))
migrate = Migrate(app, db)

#to automatically setup the db when the app is called
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, ReviewTable=ReviewTable)


#adding "flask test" as a custom command to run
#the tests for this web application
@app.cli.command()
def test():
    """Run the unit tests!"""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    
