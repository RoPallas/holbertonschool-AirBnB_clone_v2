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


@app.route("/states", strict_slashes=False)
@app.route("/states_list", strict_slashes=False)
def states_list():
    """display a HTML page, with the list of all State objects"""
    return render_template('7-states_list.html',
                           states=storage.all("State").values())


@app.route('/states/<id>')
def if_state_id(id):
    """display a HTML page, with the list of City objects linked to the State """
    state_obj = None
    for state in storage.all("State").values():
        if state.id == id:
            state_obj = state
    return render_template('9-states.html',
                           state_obj=state_obj)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
