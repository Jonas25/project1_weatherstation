from flask import Flask
import os
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)