from flask import Flask
from database.SqlGis import gdal_sqlite
import os



app = Flask(__name__)
db = gdal_sqlite()
#from app import views, models


if __name__ == '__main__':
    app.run(debug = True)
