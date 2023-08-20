#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models import *
app = Flask(__name__)


@app.teardown_appcontext
def teardown_storage(self):
    """remove the current SQLAlchemy Session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """display a HTML page, with the list of all State objects"""
    return render_template('8-cities_by_states.html',
                           states=storage.all("State").values())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
