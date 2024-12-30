from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from retail_chain.models import Company, Product, Contacts
from retail_chain.paginators import Pagination
from retail_chain.permissions import IsUserModerator, IsUserOwner
from retail_chain.serializers import (
    CompanySerializer,
    CompanyAllFieldsSerializer,
    ProductSerializer,
    ContactsSerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Контроллер для работы с моделью Company, реализует следующие функции:

    Поиск и фильтрация:
        Поддерживает поиск по полям: type, name, supplier, level, date_created
        с использованием SearchFilter.
    Права доступа:
        Список компаний: доступен для чтения всем аутентифицированным пользователям.
    Создание, обновление, удаление, просмотр компании:
        доступно пользователям с правами:
         IsUserModerator, IsUserOwner, или администратору.
    Создание записи:
        Запрещает указание задолженности (debt или debt_currency) при создании компании.
        В противном случае возвращается ошибка с кодом 403.
    Обновление записи:
        Запрещает изменение поля debt через API.
        При попытке изменения возвращается ошибка с кодом 403.
    """

    queryset = Company.objects.all()
    serializer_class = CompanyAllFieldsSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["type", "name", "supplier", "level", "date_created"]

    def get_permissions(self):
        if not self.request.user.is_staff and self.request.user.is_active:
            if self.action in ["update", "retrieve", "create", "destroy"]:
                self.permission_classes = (IsUserModerator | IsUserOwner,)
            elif self.action == "list":
                self.permission_classes = (IsAuthenticatedOrReadOnly,)
        return super().get_permissions()
        serializer_class = CompanySerializer
        if self.action:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Создание записи:
        Запрещает указание задолженности (debt или debt_currency) при создании компании.
        В противном случае возвращается ошибка с кодом 403
        Поля:
            type - Тип Компании
            name - Название компании
            level - Номер уровня иерархии
            debt - задолжность вашему поставщику, может быть 0
            products - продукты, которые предоставляет компания
        """

        serializer = self.get_serializer(data=request.data)
        if (
            request.data.get("debt") is None
            and request.data.get("debt_currency") is None
        ):
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        data = {"error": f"Ошибка с кодом 403. Вы не можете указывать задолженность"}
        return JsonResponse(
            data["error"],
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
            json_dumps_params={"ensure_ascii": False},
        )

    def perform_update(self, serializer):
        """
        Запрещает изменение поля debt.
        При попытке изменения возвращается ошибка с кодом 403
        """
        if self.request.data.get("debt"):
            data = {"error": f"Ошибка с кодом 403. Вы не можете менять задолженность"}
            return JsonResponse(
                data["error"],
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
                json_dumps_params={"ensure_ascii": False},
            )
        serializer.save()
        Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Контроллер для работы с моделью Product, реализует следующие функции:

    Поиск и фильтрация:
        product_name, product_model, product_date
        с использованием SearchFilter.
    Права доступа:
        Список продуктов: доступен для чтения всем аутентифицированным пользователям.
        Создание, обновление, удаление, просмотр продукта:
            доступно пользователям с правами
            IsUserModerator, IsUserOwner, или администратору.
    Создание записи:
        Проверяет корректность данных перед созданием:
        Поле product_name не должно быть пустым и не может
            содержать только числовые значения.
        В случае несоответствия возвращается ошибка с кодом 400.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["product_name", "product_model", "product_date"]

    def get_permissions(self):
        if self.request.user.is_active:
            if self.action in ["update", "retrieve", "create", "destroy"]:
                self.permission_classes = (IsUserModerator | IsUserOwner | IsAdminUser,)
            elif self.action == "list":
                self.permission_classes = (IsAuthenticatedOrReadOnly,)
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Проверяет корректность данных перед созданием:
        Поле product_name не должно быть пустым и не может содержать только числовые значения.
        В случае несоответствия возвращается ошибка с кодом 400.
        """

        serializer = self.get_serializer(data=request.data)
        if (
            request.data.get("product_name") is None
            or request.data.get("product_model")
            or request.data.get("product_name").isdigit()
        ):
            data = {"error": f"Ошибка с кодом 400. Укажите название продукта"}
            return JsonResponse(
                data["error"],
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
                json_dumps_params={"ensure_ascii": False},
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactsViewSet(viewsets.ModelViewSet):
    """
    Контроллер для работы с моделью Contacts, реализует следующие функции:

    Поиск и фильтрация:
        Поддерживает поиск по полю: country с использованием SearchFilter.
    Права доступа:
        Все действия (list, create, retrieve, update, destroy) доступны пользователям
        с правами IsUserModerator, IsUserOwner, или администратору.
    """

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["country"]

    def get_permissions(self):
        if self.request.user.is_active:
            if self.action:
                self.permission_classes = (IsUserModerator | IsUserOwner | IsAdminUser,)
        return super().get_permissions()
