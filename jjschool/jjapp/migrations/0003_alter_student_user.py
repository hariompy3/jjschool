# Generated by Django 5.0.6 on 2024-06-20 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jjapp", "0002_remove_student_profile_image_student_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="student",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
