from django.db import models
from slugify import slugify
from users.models import User


# Create your models here.
class Blog(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Заголовок", help_text="Введите заголовок."
    )
    content = models.TextField(
        verbose_name="Содержание", help_text="Введите текст статьи."
    )
    slug = models.CharField(max_length=100, unique=True, blank=True)
    image = models.ImageField(
        upload_to="media/",
        verbose_name="Изображение",
        help_text="Загрузите изображение статьи.",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, verbose_name="Опубликовано")
    views = models.IntegerField(default=0, verbose_name="Просмотры")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at", "-status"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
