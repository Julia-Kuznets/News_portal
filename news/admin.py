from django.contrib import admin
from .models import Author, Category, Post, Postcategory, Comment


# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Postcategory)
admin.site.register(Comment)