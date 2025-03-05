from computational_metrics import percent_linearity, percent_leniency
from grid_tools import rows_into_columns
from flask import Flask, request
from json import load, loads
import logging
import os

from summerville_agent import percent_playable

app = Flask(__name__)

@app.route('/config')
def config():
    with open('config.json', 'r') as f:
        return load(f)

@app.route('/levels')
def levels():
    lvls = []
    for file_name in os.listdir('levels'):
        with open(os.path.join('levels', file_name), 'r') as f:
            lvls.append(rows_into_columns(f.readlines()))

    return lvls

@app.route('/assess')
def assess_level():
    lvl = loads(loads(request.args.get('lvl').replace('%20', ' ')))
    return {
        'completability': percent_playable(lvl),
        'linearity': percent_linearity(lvl),
        'leniency': percent_leniency(lvl),
    }

if __name__ == '__main__':
    # disable logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # start flask server
    app.run(debug=True, port=5000)