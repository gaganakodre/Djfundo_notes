# Generated by Django 4.1.1 on 2022-09-20 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lables', '0001_initial'),
        ('notes', '0003_notes_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, to='lables.labels'),
        ),
    ]
