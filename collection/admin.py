from django.contrib import admin
from collection.models import Thing


# set up automated slug creation
class ThingAdmin(admin.ModelAdmin):
    model = Thing
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
admin.site.register(Thing, ThingAdmin)
