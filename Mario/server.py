from flask import Flask, request
from json import load, loads

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

if __name__ == '__main__':
    app.run(debug=True)