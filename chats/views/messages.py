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

        