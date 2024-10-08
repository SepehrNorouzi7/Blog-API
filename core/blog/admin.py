from django.contrib import admin
from blog.models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "category",
        "status",
        "created_date",
        "published_date",
    ]


admin.site.register(Category)
admin.site.register(Post)
