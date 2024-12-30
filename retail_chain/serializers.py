from rest_framework import serializers
from retail_chain.models import Company, Contacts, Product


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CompanyAllFieldsSerializer(serializers.ModelSerializer):
    company_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        exclude = ("debt", "debt_currency")


class CompanySerializer(serializers.ModelSerializer):
    company_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
