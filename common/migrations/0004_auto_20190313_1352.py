# Generated by Django 2.1.4 on 2019-03-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_readnum_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnum',
            name='created_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
