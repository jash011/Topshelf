# Generated by Django 5.2.3 on 2025-07-02 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ziplink', '0002_link_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='short_url',
            field=models.CharField(max_length=225, unique=True),
        ),
    ]
