from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "created_at",
        "status",
        "views",
        "slug",
    )
    list_filter = ("status",)
    search_fields = (
        "title",
        "content",
    )
    prepopulated_fields = {"slug": ("title",)}
