import urllib3
import json

def send(message, chat_id, token):
    http = urllib3.PoolManager()
    url = "https://api.telegram.org/bot{0}/sendMessage".format(token)
    http.request('POST', url, headers={'Content-Type': 'application/json'},
    body=json.dumps({
        "chat_id": chat_id,
        "text": message
    }))