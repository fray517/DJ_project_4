from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TelegramUser
from .serializers import TelegramUserSerializer

@api_view(['POST'])
def register_user(request):
    data = request.data
    user, created = TelegramUser.objects.get_or_create(
        user_id=data['user_id'],
        defaults={'username': data.get('username', '')}
    )
    if created:
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data, status=201)
    else:
        return Response({'message': 'User is already registered'}, status=200)