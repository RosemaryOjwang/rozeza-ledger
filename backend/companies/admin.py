from django.contrib import admin
from .models import Company

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
