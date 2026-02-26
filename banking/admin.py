from django.contrib import admin

from .models import Account, Customer, Statement, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "id_number", "created_at")
    search_fields = ("full_name", "phone", "id_number")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "account_type", "balance", "created_at")
    list_filter = ("account_type",)
    search_fields = ("number", "customer__full_name")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "tx_type", "amount", "created_at", "description")
    list_filter = ("tx_type",)
    search_fields = ("account__number",)


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ("account", "original_name", "object_name", "uploaded_at")
    search_fields = ("account__number", "original_name", "object_name")


