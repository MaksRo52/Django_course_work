from django.urls import reverse_lazy
from blog.forms import BlogForm
from blog.models import Blog
from django.views import generic
from blog.services import get_blog_from_cache


# Create your views here.


class BlogDetailView(generic.DetailView):
    model = Blog
    object = None

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogListView(generic.ListView):
    model = Blog

    def get_queryset(self):
        return get_blog_from_cache()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        status_list = Blog.objects.filter(status="True").order_by("-created_at")
        context["status_list"] = status_list
        return context


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(generic.UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def get_success_url(self):
        return reverse_lazy("blog:blog_view", args=[self.kwargs["slug"]])


class BlogCreateView(generic.CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            from slugify import slugify

            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def form_user(self, form):
        blog = form.save()
        blog.autor = self.request.user
        blog.save()
        return super().form_valid(form)
