from django.db import models
from djmoney.models.fields import MoneyField

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    product_name = models.CharField(
        max_length=250,
        verbose_name="Название продукта",
        help_text="Укажите название продукта",
    )
    product_model = models.CharField(
        max_length=150,
        verbose_name="Модель продукта",
        help_text="Укажите модель продукта",
    )
    product_date = models.DateField(
        default=None,
        verbose_name="Дата выхода продукта на рынок",
        help_text="Укажите дату выхода продукта на рынок",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.product_name


class Company(models.Model):
    class LevelChoices(models.IntegerChoices):
        FABRIC = 0, "Завод - 0 уровень"
        SUPPLIER_FIRST = 1, "Поставщик от фабрики - 1 уровень"
        SUPPLIER_SECOND = 2, "Поставщик поставщика - 2 уровень"

    type_company = {
        "fabric": "Завод",
        "retail": "Розничная сеть",
        "individual_entrepreneur": "Индивидуальный предприниматель",
    }
    type = models.CharField(
        max_length=150,
        verbose_name="Тип компании",
        help_text="Укажите тип компании",
        choices=type_company,
    )
    name = models.CharField(
        max_length=250,
        verbose_name="Название компании",
        help_text="Укажите название компании",
    )
    supplier = models.ForeignKey(
        "Company",
        on_delete=models.PROTECT,
        verbose_name="Поставщик",
        help_text="Укажите поставщика",
        **NULLABLE,
    )
    level = models.PositiveIntegerField(
        verbose_name="Номер уровня иерархии",
        help_text="Укажите номер уровня иерархии",
        choices=LevelChoices.choices,
    )
    description = models.TextField(
        verbose_name="Описание компании",
        help_text="Укажите описание компании",
        **NULLABLE,
    )
    debt = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="RUB",
        default=0.00,
        verbose_name="Задолжность",
        help_text="Укажите задолжность вашему поставщику",
    )
    date_created = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="Продукты",
        help_text="Укажите продукты, которые предоставляет компания",
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"


class Contacts(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        help_text="Укажите компанию",
        related_name="company_contacts",
    )
    email = models.EmailField(
        verbose_name="e-mail организации",
        help_text="Укажите e-mail организации",
        unique=True,
    )
    inn = models.PositiveIntegerField(
        verbose_name="ИНН организации", help_text="Укажите ИНН организации"
    )
    country = models.CharField(
        max_length=150,
        verbose_name="Страна",
        help_text="Укажите страну",
        **NULLABLE,
    )
    city = models.CharField(
        max_length=150,
        verbose_name="Город",
        help_text="Укажите город",
        **NULLABLE,
    )
    street = models.CharField(
        max_length=150,
        verbose_name="Улица",
        help_text="Укажите улицу",
        **NULLABLE,
    )
    number_house = models.PositiveIntegerField(
        verbose_name="Номер дома",
        help_text="Укажите номер дома",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return f"{self.email} - {self.inn}"
