# Generated by Django 2.1.3 on 2018-11-27 05:09

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shiju', '0008_artical_huishou'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(default='', max_length=100)),
                ('zhiwei', models.CharField(default='', max_length=100)),
                ('zhiban_date', models.CharField(choices=[('0', '星期一'), ('1', '星期二'), ('2', '星期三'), ('3', '星期四'), ('4', '星期五'), ('5', '星期六'), ('6', '星期日'), ('7', '无')], default='7', max_length=10)),
                ('jigou', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shiju.Jigou')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='artical',
            name='neirong',
            field=DjangoUeditor.models.UEditorField(blank=True, verbose_name='内容\t'),
        ),
    ]