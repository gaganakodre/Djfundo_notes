# Generated by Django 4.1.1 on 2022-09-10 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
