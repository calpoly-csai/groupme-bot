from flask import Flask, jsonify, request

import config
import json
import requests

app = Flask(__name__)

# to allow all methods
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


@app.route("/")
def hello():
    return "Hello GroupMe-Bot!"


@app.route("/post-groupme-message")
def post_a_message():
    pass

def make_get_messages_by_group_id_url_params():
    """Make the API URL"""
    base = "https://api.groupme.com/v3"
    base_grp = base + "/groups"
    base_grp_id = base_grp + "/{}"
    base_grp_id_msg = base_grp_id + "/messages"
    URL = base_grp_id_msg.format(
        config.GROUPME_GROUP_ID,
    )
    PARAMS = {"token": config.GROUPME_ACCESS_TOKEN}
    return URL, PARAMS


def find_latest_message():
    URL, PARAMS = make_get_messages_by_group_id_url_params()
    response = requests.get(url=URL, params=PARAMS)
    response_body = response.json()
    return response_body.get('response', {}).get('messages', [None])[0]


@app.route("/test-slack")
def send_to_slack(text="hello world"):
    '''
    POST https://slack.com/api/chat.postMessage
    Content-type: application/json
    Authorization: Bearer YOUR_TOKEN_HERE
    {
        "channel": "YOUR_CHANNEL_ID",
        "text": "Hello, world"
    }
    '''

    URL = "https://slack.com/api/chat.postMessage"
 
    message = {
                "channel": config.SLACK_GENERAL_CHANNEL_ID,
                "text": text
              }
    
    headers = {
                "Content-Type" : "application/json",
                "Authorization" : "Bearer " + config.SLACK_ACCESS_TOKEN
              }
    
    requests.post(URL, data=json.dumps(message), headers=headers)
    
    return "SUCCESS", 200

@app.route("/get-latest-message-object/", methods=['GET'])
def get_latest_message_object():
    latest_message = find_latest_message()

    if latest_message is not None and type(latest_message) is dict:
        return jsonify(latest_message), 200
    else:
        print("latest_message", latest_message)
        return "latest_message is unexpected... oops", 201


@app.route("/new-groupme-message", methods=HTTP_METHODS)
def got_new_message():
    print("got a message!")

    latest_message = find_latest_message()

    if latest_message is not None and type(latest_message) == dict:
        latest_message_text = latest_message.get("text", None)
        latest_message_sender = latest_message.get("name", None)

        slack_message =  "%s: %s" % \
                            (latest_message_sender, latest_message_text)

        send_to_slack(slack_message)

    if latest_message_text is not None:
        return slack_message, 200
    else:
        return "latest_message_text is None... oops", 201

def cute_pics(message):
    if "@csaibot" in message[0:8]:
        if "cat" in message:
            return "https://66.media.tumblr.com/tumblr_lta61d2BgL1r4ghkoo1_500.gifv"
        elif "dog" in message:
            return "https://data.whicdn.com/images/116913623/original.gif"
        else:
            return "https://i.kym-cdn.com/photos/images/original/001/743/050/b3f.jpeg"
    else: #when @csaibot is not in the message
        return "format: @csaibot <message>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
