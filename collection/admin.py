from django.contrib import admin
from collection.models import Thing, Social, Upload


# set up automated slug creation
class ThingAdmin(admin.ModelAdmin):
    model = Thing
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}


class SocialAdmin(admin.ModelAdmin):
    model = Social
    list_display = ('network', 'username',)

class UploadAdmin(admin.ModelAdmin):
    list_display = ('thing',)
    list_display_links = ('thing',)

# Register your models here.
admin.site.register(Thing, ThingAdmin)
admin.site.register(Social, SocialAdmin)
admin.site.register(Upload, UploadAdmin)

