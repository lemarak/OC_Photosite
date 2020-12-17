from django.contrib import admin

from .models import Picture, Contest, Review, Category, Vote, ContestPicture

class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ('upload_date',)

class ContestAdmin(admin.ModelAdmin):
    readonly_fields = ('date_creation',)


admin.site.register(Picture, PictureAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(ContestPicture)
