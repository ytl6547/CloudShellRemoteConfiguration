# Generated by Django 2.2.1 on 2019-06-04 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebTerm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='name',
        ),
        migrations.AlterField(
            model_name='device',
            name='lastAccessTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]