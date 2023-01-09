from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask import Flask, request, jsonify
from .config import Config
import requests
import os
from .models import EODData, User
import datetime
import time

app = Flask(__name__)

from .auth import auth_required

access_key = Config.ACCESS_KEY
db_username = Config.DB_USERNAME
db_password = Config.DB_PASSWORD
db_server = Config.DB_SERVER
db_name = 'eodtracker_test'
# DB_URL = Config.DB_URL
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_username, pw=db_password, url=db_server,db=db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['APPSETTING_ENVIRONMENT'] = Config.APPSETTING_ENVIRONMENT
app.config['SECRET_KEY'] = 'JamesB0ndoo7'

db.init_app(app)

with app.app_context():
    db.create_all()


def convert_to_unix(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))


def convert_to_datestr(date):
    return str(datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%dT%H:%M:%S+%fZ'))[:-3]


@app.route('/eod', methods=['GET'])
@auth_required
def get_eod_data():
    try:
        if request.args.get('symbol'):
            symbol = request.args.get('symbol')
        else:
            return 'Ticker symbol required.', 400

        highest_date = db.session.query(db.func.max(EODData.date)).filter(EODData.symbol == symbol).scalar()
        lowest_date = db.session.query(db.func.min(EODData.date)).filter(EODData.symbol == symbol).scalar()
        original_from_date = 0
        if request.args.get('from_date'):
            from_date = request.args.get('from_date')
            from_date_unix = convert_to_unix(from_date)
            original_from_date = from_date_unix
        else:
            from_date = ''
            from_date_unix = lowest_date
        if request.args.get('to_date'):
            to_date = request.args.get('to_date')
            to_date_unix = convert_to_unix(to_date)
        else:
            to_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            to_date_unix = convert_to_unix(datetime.datetime.utcnow().strftime('%Y-%m-%d'))

        eod_data_list = []

        # Check if the data is in the database
        DB_Check = True
        if len(EODData.query.filter_by(symbol=symbol).limit(1).all()) < 1:
            from_date = "2008-01-01"
            from_date_unix = convert_to_unix(from_date)
            DB_Check = False


        if DB_Check and highest_date is not None and lowest_date is not None and (from_date_unix >= lowest_date) and (
                highest_date >= to_date_unix):
            eod_data = EODData.query.filter_by(symbol=symbol).filter(EODData.date >= from_date_unix).filter(
                EODData.date <= to_date_unix).all()
            if eod_data:
                for each_record in eod_data:
                    each_record_dict = each_record.__dict__.copy()
                    each_record_dict['date'] = convert_to_datestr(each_record_dict['date'])
                    each_record_dict.pop('_sa_instance_state', None)
                    each_record_dict.pop('id', None)
                    eod_data_list.append(each_record_dict)

                return jsonify(DB_data=eod_data_list)

        # If the data is not in the database, make the API call to the Marketstack EOD API
        api_url = f'http://api.marketstack.com/v1/eod?access_key={access_key}&symbols={symbol}&date_from={from_date}&date_to={to_date}'
        print(datetime.datetime.now())
        print(api_url)
        response = requests.get(api_url)
        data = response.json()

        for record in data['data']:
            record_date_unix = convert_to_unix(record['date'].split("T")[0])
            if record_date_unix >= original_from_date:
                eod_data_list.append({"symbol": record['symbol'],
                                      "date": record['date'],
                                      "open": record['open'],
                                      "high": record['high'],
                                      "low": record['low'],
                                      "close": record['close'],
                                      "volume": record['volume']})

            existing_record = EODData.query.filter_by(symbol=record['symbol']).filter_by(date=record_date_unix).first()
            if existing_record is None:
                eod_data = EODData(symbol=record['symbol'],
                                   date=record_date_unix,
                                   open=record['open'],
                                   high=record['high'],
                                   low=record['low'],
                                   close=record['close'],
                                   volume=record['volume'])

                db.session.add(eod_data)
        try:
            db.session.commit()
        except:
            pass
        return jsonify(API_data=eod_data_list)
    except Exception as e:
        print(e)
        return "Invalid request", 400


@app.route('/change-in-price', methods=['GET'])
@auth_required
def change_in_price():
    # Get the symbol and number of days from the request query parameters
    symbol = request.args.get('symbol')
    num_days = request.args.get('num_days')
    if app.config['APPSETTING_ENVIRONMENT'] == 'production':
        return 'This endpoint is not available in the current environment', 404

    # Get the data for the given symbol from the database and Calculate the change in price
    eod_data = EODData.query.filter_by(symbol=symbol).order_by(EODData.date.desc()).limit(num_days).all()
    if eod_data:
        change_in_price = eod_data[0].close - eod_data[-1].close
        return f'The change in price for {symbol} over the past {num_days} days is {change_in_price}. Note-Difference calculation is done only for the data available in database. '
    else:
        return 'Symbol/Ticker is not available in DB'


@app.route('/')
def index():
    try:
        webapp_env = os.environ['APPSETTING_ENVIRONMENT']
        img_id = os.environ['imageid']
    except:
        webapp_env = ''
        img_id = ''
    return '<h1>Hello, You are in ' + str(webapp_env) + ' environment. We are using image - '+str(img_id)+'</h1>'


if __name__ == "__main__":
    port = 80
    app.run(host="0.0.0.0", port=port)
