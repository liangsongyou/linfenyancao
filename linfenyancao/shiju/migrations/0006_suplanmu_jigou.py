# Generated by Django 2.1.3 on 2018-11-23 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shiju', '0005_auto_20181123_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='suplanmu',
            name='jigou',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shiju.Jigou'),
        ),
    ]
