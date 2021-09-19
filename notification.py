import telegram_notifications

class NotificationManager:
    def __init__(self, medium, message, recipient_id, authorization_info):
        self.medium = medium
        self.message = message
        self.recipient_id = recipient_id
        self.authorization_info = authorization_info

    def send(self):
        if self.medium == 'telegram':
            telegram_notifications.send(self.message, self.recipient_id, self.authorization_info)