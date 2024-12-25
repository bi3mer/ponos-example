from grid_tools import rows_into_columns
from flask import Flask, request
from json import load, loads
import os

from summerville_agent import percent_playable

app = Flask(__name__)

@app.route('/config')
def config():
    with open('config.json', 'r') as f:
        return load(f)

@app.route('/completability')
def completability():
    playable = percent_playable(loads(request.args.get('lvl')))
    return str(playable)

@app.route('/levels')
def levels():
    lvls = []
    for file_name in os.listdir('levels'):
        with open(os.path.join('levels', file_name), 'r') as f:
            lvls.append(rows_into_columns(f.readlines()))

    return lvls

if __name__ == '__main__':
    app.run(debug=True)