# Generated by Django 4.2 on 2025-05-16 15:52

from django.db import migrations, models
import library.utils


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='due_date',
            field=models.DateField(default=library.utils.get_due_date),
        ),
    ]
