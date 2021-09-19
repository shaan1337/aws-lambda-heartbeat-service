import heartbeat
import config
import notification

def get_path(event):
  if 'pathParameters' in event \
  and event['pathParameters'] \
  and 'proxy' in event['pathParameters']:
    return event['pathParameters']['proxy']
  else:
    return None

def get_http_method(event):
    if 'httpMethod' in event:
        return event['httpMethod']
    return None

def lambda_handler(event, context):
    heartbeat_mgr = heartbeat.HeartbeatManager(config.heartbeat_dynamodb_table, config.heartbeat_timeout)
    notification_mgr = notification.NotificationManager(
        config.notification_medium,
        config.notification_message,
        config.notification_recipient_id,
        config.notification_authorization_info)

    response = None
    try:
        response = process_request(event, context, heartbeat_mgr, notification_mgr)
        if response is None:
            response = {
                'statusCode': 400
            }
    except:
        response = {
            'statusCode': 500
        }

    return response

def process_request(event, context, heartbeat_mgr, notification_mgr):
    path = get_path(event)
    http_method = get_http_method(event)

    if path == 'set' and http_method == 'POST':
        heartbeat_mgr.set()
        return {'statusCode': 200,'body': '{}'}
    elif path == 'check' and http_method == 'GET':
        if(not(heartbeat_mgr.check())):
             notification_mgr.send()
        return {'statusCode': 200,'body': '{}'}
    return None