# Generated by Django 3.1.1 on 2020-09-11 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_poll_abstract'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='title',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]