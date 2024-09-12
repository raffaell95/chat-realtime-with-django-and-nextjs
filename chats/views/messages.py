from core.socket import socket
from core.utils.exceptions import ValidationError

from chats.views.base import BaseView
from chats.models import Chat, ChatMessage
from chats.serializers import ChatMessageSerializer

from attachments.models import FileAttachment, AudioAttachment

from rest_framework.response import Response

from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import uuid

class ChatMesageView(BaseView):
    def get(self, request, chat_id):
        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        self.mark_messages_as_seen(chat_id, request.user.id)

        socket.emit('mark_messages_as_seen', {
            "query": {
                "chat_id": chat_id,
                "exclude_user_id": request.user.id
            }
        })

        messages = ChatMessage.objects.filter(
            chat_id=chat_id,
            deleted_at__isnull=True
        ).order_by('created_at').all()

        serializer = ChatMessageSerializer(messages, many=True)

        socket.emit('update_at', {
            "query": {
                "users": [chat.from_user_id, chat.to_user_id]
            }
        })

        return Response({
            "messages": serializer.data
        })
    
    def post(self, request, chat_id):
        body = request.data.get('body')
        file = request.FILES.get('file')
        audio = request.FILES.get('audio')

        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        self.mark_messages_as_seen(chat_id, request.user.id)

        if not body and not file and audio:
            raise ValidationError("Nenhum parametro foi informado")
        
        attachment = None

        if file:
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / 'files',
                settings.MEDIA_URL + 'files'
            )

            content_type = file.content_type
            name = file.name.split('.')[0]
            extension = file.name.split('.')[-1]
            size = file.size