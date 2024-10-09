from django.urls import path
from blog.apps import BlogConfig
from blog.views import (
    BlogCreateView,
    BlogUpdateView,
    BlogListView,
    BlogDetailView,
    BlogDeleteView,
)

app_name = BlogConfig.name

urlpatterns = [
    path("create/", BlogCreateView.as_view(), name="blog_create"),
    path("", BlogListView.as_view(), name="blog_list"),
    path("view/<slug>/", BlogDetailView.as_view(), name="blog_view"),
    path("update/<slug>/", BlogUpdateView.as_view(), name="blog_update"),
    path("delete/<slug>/", BlogDeleteView.as_view(), name="blog_delete"),
]
