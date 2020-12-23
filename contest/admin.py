from django.contrib import admin

from .models import Contest, Vote, ContestPicture


class ContestAdmin(admin.ModelAdmin):
    readonly_fields = ('date_creation',)


admin.site.register(Contest, ContestAdmin)
admin.site.register(Vote)
admin.site.register(ContestPicture)
