from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    return "Simple Flask App running"


if __name__ == '__main__':
    app.run(debug=True)