#!flask/bin/python

from app import app,db
from config import load_config




config = load_config()
app.config.from_object(config)


#app.run(debug = True)