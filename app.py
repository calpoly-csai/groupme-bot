from flask import Flask

import config

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello GroupMe-Bot!"


@app.route("/post-groupme-message")
def post_a_message():
    pass


def find_latest_message():
    pass


@app.route("/new-groupme-message")
def got_new_message():
    print("got a message!")
    find_latest_message()
    post_a_message()
    return msg


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
