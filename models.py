from .app import db

# Define the EOD data model
class EODData(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  symbol = db.Column(db.String(20), nullable=False)
  date = db.Column(db.Integer, nullable=False)
  open = db.Column(db.Float, nullable=False)
  high = db.Column(db.Float, nullable=False)
  low = db.Column(db.Float, nullable=False)
  close = db.Column(db.Float, nullable=False)
  volume = db.Column(db.Float, nullable=False)


# Define the User model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(60), nullable=False, unique=True)
  password = db.Column(db.String(260), nullable=False)



