import json
from datetime import date

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User

from .models import Profile, ChatMessage
from .img import update_png

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'main_chat',
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'main_chat',
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['mtype'] == 'msg':
            message = text_data_json['msg']
            sender = User.objects.get(profile=Profile.objects.get(code=text_data_json['code']))

            cm = ChatMessage.objects.create(
                message=message, sender=f'{sender.first_name} {sender.last_name}'
            )
            cm.save()

            async_to_sync(self.channel_layer.group_send)(
                'main_chat',
                {
                    'type': 'chat_message',
                    'msg': message,
                    'sender': f'{sender.first_name} {sender.last_name}',
                }
            )
        elif text_data_json['mtype'] == 'px':
            x, y = map(int, text_data_json['px'].split('-'))
            update_png('/var/www/html/assets/images/' + date.today().strftime('%b-%Y.png'), x, y, text_data_json['color'])

            async_to_sync(self.channel_layer.group_send)(
                'main_chat',
                {
                    'type': 'px_update',
                    'pxId': text_data_json['px'],
                    'color': text_data_json['color'],
                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps(dict(event)))
    
    def px_update(self, event):
        self.send(text_data=json.dumps(dict(event)))