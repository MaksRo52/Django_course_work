# Generated by Django 5.1.2 on 2024-10-08 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attempt",
            name="server_response",
            field=models.TextField(blank=True, null=True, verbose_name="Ответ сервера"),
        ),
    ]
