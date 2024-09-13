from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication, BaseAuthentication

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.timezone import now

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from accounts.models import User

from core.utils.exceptions import ValidationError

import uuid

class SignInView(APIView, Authentication):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        signin = self.signin(email, password)

        if not signin:
            raise AuthenticationFailed
        
        user = UserSerializer(signin).data
        access_token = RefreshToken.for_user(signin).access_token

        return Response({
            "user": user,
            "access_token": str(access_token)
        })

class SignUpView(APIView, Authentication):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        if not name or not email or not password:
            raise AuthenticationFailed
        
        signup = self.signup(name, email, password)
        print(signup)

        if not signup:
            raise AuthenticationFailed
        
        user = UserSerializer(signup).data
        access_token = RefreshToken.for_user(signup).access_token

        return Response({
            "user": user,
            "access_token": str(access_token)
        })
    
class UserView(APIView):
    def get(self, request):
        
        User.objects.filter(id=request.user.id).update(last_access=now())

        user = UserSerializer(request.user).data

        return Response({
            'user': user
        })
    
    def put(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        avatar = request.FILES.get('avatar')

        storage = FileSystemStorage(
            settings.MEDIA_ROOT / 'avatars',
            settings.MEDIA_URL + 'avatars'
        )

        if avatar:
            content_type = avatar.contenr_type
            extension = avatar.name.split('.')[-1]

            if not content_type == 'image/png' and not content_type == 'image/jpeg':
                raise ValidationError(
                'Somente arquivos do tipo PNG ou JPEG são suportados'
            )

            file = storage.save(f"{uuid.uuid4()}.{extension}", avatar)
            avatar = storage.url(file)

        serializer = UserSerializer(request.user, data={
            'name': name,
            'email': email,
            'avatar': avatar or request.user.avatar
        })

        if not serializer.is_valid():
            if avatar:
                storage.delete(avatar.split('/')[-1])
            
            first_error = list(serializer.errors.values())[0][0]

            raise ValidationError(first_error)

        if avatar and request.user.avatar != '/media/avatars/default-avatar.png':
            storage.delete(request.user.avatar.split('/')[-1])
        
        if password:
            request.user.set_password(password)
        
        serializer.save()

        return Response({
            'user': serializer.data
        })
