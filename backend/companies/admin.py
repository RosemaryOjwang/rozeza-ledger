from django.contrib import admin
from .models import Company, Membership

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_dispaly = (
        "name",
        "kra_pin",
        "country",
        "currency",
        "is_active",
    )

    search_fields = (
        "name",
        "kra_pin"        
    )

    list_filter = (
        "country",
        "is_active"

    )

@admin.register(Membership)
class MembeshipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company",
        "role",
        "is_active",
        "joined_at"
    )

    search_fields = (
        "user__email",
        "company__name"
    )

    list_filter = (
        "role",
        "is_active"
    )
