from django.db import models
from users.models import User

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    """Клиент сервиса"""

    name = models.CharField(
        max_length=255, verbose_name="ФИО", help_text="Введите имя клиента"
    )
    email = models.EmailField(
        max_length=100, verbose_name="Почта для рассылки", help_text="Заполните почту"
    )
    comment = models.TextField(max_length=250, verbose_name="Комментарий")
    autor = models.ForeignKey(
        User, verbose_name="автор", on_delete=models.SET_NULL, **NULLABLE
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Message(models.Model):
    """Сообщение для рассылки"""

    title = models.CharField(max_length=100, verbose_name="Тема письма")
    content = models.TextField(max_length=500, verbose_name="Содержание письма")
    autor = models.ForeignKey(
        User, verbose_name="автор", on_delete=models.SET_NULL, **NULLABLE
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Mailing(models.Model):
    """Рассылка"""

    is_active = models.BooleanField(default=True, verbose_name="Активность рассылки")
    date_of_first_mail = models.DateTimeField(verbose_name="Дата отправки")
    date_of_last_mail = models.DateTimeField(verbose_name="Дата окончания рассылки")
    periodicity = models.CharField(
        max_length=5,
        verbose_name="Периодичность",
        choices={"day": "Раз в день", "week": "Раз в неделю", "month": "Раз в месяц"},
    )
    status = models.CharField(
        max_length=8,
        verbose_name="Статус рассылки",
        choices={"new": "Создана", "active": "Запущена", "complete": "Завершена"},
    )
    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        help_text="Выберите сообщение",
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    autor = models.ForeignKey(
        User, verbose_name="автор", on_delete=models.SET_NULL, **NULLABLE
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["date_of_first_mail"]
        permissions = [
            ("can_view_mailing", "Can view mailing"),
            ("can_disable_mailing", "Can disable mailing"),
        ]

    def __str__(self):
        return str(self.date_of_first_mail)


class Attempt(models.Model):
    """Попытка отправки письма"""

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата первой попытки"
    )
    status = models.BooleanField(verbose_name="Статус попытки")
    server_response = models.TextField(verbose_name="Ответ сервера", **NULLABLE)
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "Попытки отправки"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)
