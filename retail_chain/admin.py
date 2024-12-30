from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from retail_chain.models import Company, Product, Contacts


class ContactAdmin(admin.StackedInline):
    model = Contacts
    extra = 1


@admin.register(Contacts)
class ContactsConcreteAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "inn",
        "country",
        "city",
        "street",
        "number_house",
    )
    list_filter = ("country", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "product_date",
    )
    list_filter = (
        "product_name",
        "product_model",
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_type_display",
        "name",
        "supplier_link",
        "level",
        "date_created",
    )

    inlines = [ContactAdmin]

    @admin.display(description=("Поставщик"))
    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse(
                f"admin:{obj.supplier._meta.app_label}_{obj.supplier._meta.model_name}_change",
                args=(obj.supplier.pk,),
            )
            return mark_safe(f'<a href="{url}" target="_blank">{obj.supplier}</a>')
        return "-"

    @admin.action(description="Обнулить задолженость компании")
    def make_debt_to_zero(self, request, queryset):
        print(request)
        queryset.update(debt=0)

    actions = [make_debt_to_zero]
