from flask import Flask

import config
import requests

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

    # Make the API URL
    base = "https://api.groupme.com/v3"
    base_grp = base + "/groups"
    base_grp_id = base_grp + "/{}"
    base_grp_id_msg = base_grp_id + "/messages"
    URL = base_grp_id_msg.format(
        config.GROUPME_GROUP_ID,
    )
    PARAMS = {"token": config.GROUPME_ACCESS_TOKEN}
    response = requests.get(url=URL, params=PARAMS)
    response_body = response.json()

    # find_latest_message
    latest_message = response_body.get('response').get('messages', [None])[0]

    if latest_message is not None:
        return latest_message, 200
    else:
        return "latest_message is None... oops", 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
