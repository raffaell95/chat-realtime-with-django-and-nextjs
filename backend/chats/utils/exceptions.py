from rest_framework.exceptions import APIException

class UserNotFound(APIException):
    status_code = 404
    default_detail = 'Usuario nao encontrado'
    default_code = 'user_not_found'

class ChatNotFound(APIException):
    status_code = 404
    default_detail = 'Chat nao encontrado e/ou nao pertence ao usuario'
    default_code = 'chat_not_found'