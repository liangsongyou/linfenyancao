# Generated by Django 2.1.3 on 2018-11-28 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shiju', '0010_auto_20181127_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='lanmu',
            name='zhiding',
            field=models.BooleanField(default=False),
        ),
    ]