# Import the app and the database from the app.py file
from api import app, db

# create the database
with app.app_context():
    db.create_all()

