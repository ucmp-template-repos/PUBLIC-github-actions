import requests


def send_message(slack_url, message):
    # Send to slack
    req = requests.post(url=slack_url, data=message.encode('utf-8'))
    print(req)
