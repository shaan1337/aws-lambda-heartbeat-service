import boto3
from datetime import datetime

class HeartbeatManager:
    def __init__(self, dynamodb_table, timeout):
        self.dynamodb_table = dynamodb_table
        self.timeout = timeout

    def __parse_iso_timestamp__(self, timestamp):
        s = timestamp
        return datetime(
            year=int(s[0:4]),
            month=int(s[5:7]),
            day=int(s[8:10]),
            hour=int(s[11:13]),
            minute=int(s[14:16]),
            second=int(s[17:19]),
            microsecond=int(s[20:])
        )

    def check(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.dynamodb_table)
        response = table.get_item(Key={
                'id': 1
        },
        ConsistentRead = True)

        if('Item' not in response):
            return False

        last_heartbeat = response['Item']['last_heartbeat']
        if((datetime.now() - self.__parse_iso_timestamp__(last_heartbeat)).seconds <= self.timeout):
            return True
        return False

    def set(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.dynamodb_table)
        table.put_item(Item={
                'id': 1,
                'last_heartbeat': datetime.now().isoformat(),
        })