# Generated by Django 3.1.5 on 2021-07-18 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping', '0021_auto_20210718_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='addedby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
