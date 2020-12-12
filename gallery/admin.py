from django.contrib import admin

from .models import Picture, Contest, Review, Category, Vote, ContestPicture

admin.site.register(Picture)
admin.site.register(Contest)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(ContestPicture)
