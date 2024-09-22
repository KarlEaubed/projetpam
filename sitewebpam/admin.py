from django.contrib import admin


from .models import Plan
class PlanWebpam(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name', 'description', 'price')

admin.site.register(Plan, PlanWebpam)


# Register your models here.
