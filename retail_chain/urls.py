from django.urls import path, include
from rest_framework.routers import DefaultRouter

from retail_chain.apps import RetailChainConfig
from retail_chain.views import CompanyViewSet, ProductViewSet, ContactsViewSet

app_name = RetailChainConfig.name

router1 = DefaultRouter()
router1.register(r"companies", CompanyViewSet, basename="companies")
router2 = DefaultRouter()
router2.register(r"products", ProductViewSet, basename="products")
router3 = DefaultRouter()
router3.register(r"contacts", ContactsViewSet, basename="contacts")
urlpatterns = [
    path("", include(router1.urls)),
    path("", include(router2.urls)),
    path("", include(router3.urls)),
]
