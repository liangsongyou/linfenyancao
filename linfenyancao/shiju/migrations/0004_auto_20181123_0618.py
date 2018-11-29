# Generated by Django 2.1.3 on 2018-11-23 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shiju', '0003_auto_20181123_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jigou',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lanmu',
            name='jigou',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='shiju.Jigou'),
        ),
        migrations.AlterField(
            model_name='suplanmu',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
