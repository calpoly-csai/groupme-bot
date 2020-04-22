import requests
import json
import time

bot_url = "https://api.groupme.com/v3/bots/post"
bot_id = "70a82f9eaf49252e78da89a3cc"
bot_text = "Test Message from NIMBUS Slack/GroupMe auto messenger via Python"
bot_data = {"text":bot_text, "bot_id":bot_id}

read_url = "https://api.groupme.com/v3/groups/51799203/messages?token="
get_url = read_url + access_token

last_time_updated = 0
latest_time = 0
message_posting = ""

#response_post = requests.post(bot_url, json=bot_data)
#print(response_get.json()["response"]["messages"])

while True:

    response_get = requests.get(get_url)
    for message in response_get.json()["response"]["messages"]:
        
        if int(message["created_at"]) > last_time_updated:

            if int(message["created_at"]) > latest_time:
                latest_time = int(message["created_at"])
            
            message_posting += message["name"] + ": " + message["text"] + "\n"

    bot_text = message_posting
    print(bot_text)
    bot_data = {"text":bot_text, "bot_id":bot_id}
   
    if message_posting != "":
        response_post = requests.post(bot_url, json=bot_data)
        message_posting = ""
        last_time_updated = latest_time
        
    time.sleep(20)

    

'''
for message in response_get.json()["response"]:
#    if message["group_id"] == "51799203":
#        print(message)
    print(message)
    print()
    print()
'''
