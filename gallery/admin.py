from django.contrib import admin

from .models import Picture,  Category


class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ('upload_date',)


admin.site.register(Picture, PictureAdmin)
admin.site.register(Category)
