from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from retail_chain.permissions import IsUserModerator
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания новых пользователей
        Позволяет любому пользователю (без авторизации) создавать учетные записи.
    При сохранении:
        Устанавливает пользователя активным (is_active=True).
        Устанавливает пароль безопасно с использованием метода set_password.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Сначала сохраняем пользователя
        user = serializer.save(is_active=True)

        # Устанавливаем пароль с помощью set_password
        user.set_password(serializer.validated_data["password"])
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер для получения информации о текущем пользователе.
    Возвращает данные текущего аутентифицированного пользователя.
    Права доступа: требуется аутентификация.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListAPIView(generics.ListAPIView):
    """
    Контроллер для получения списка всех пользователей.
    Возвращает список всех пользователей в системе.
    Использует сериализатор UserSerializer для обработки и представления данных.
    Права доступа:
        Доступен только пользователям с правами
            модератора (IsUserModerator)
            администратора (IsAdminUser).
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = IsUserModerator | IsAdminUser
