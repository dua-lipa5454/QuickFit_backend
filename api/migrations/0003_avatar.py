# Generated by Django 5.1.7 on 2025-03-20 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_customuser_clothing_image_customuser_user_image_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Avatar",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="avatars/")),
            ],
        ),
    ]
