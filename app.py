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
def get_new_message():
    print("got a message!")
    find_latest_message()
    post_a_message()
    # will remove this code on next commit, just curious to see
    msg = "{}\n{}\n{}\n{}".format(
        config.GROUPME_ACCESS_TOKEN,
        config.GROUPME_CALLBACK_URL,
        config.GROUPME_CLIENT_ID,
        config.GROUPME_REDIRECT_URL
    )
    return msg


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
