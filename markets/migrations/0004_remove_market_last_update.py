# Generated by Django 4.1.1 on 2022-12-15 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("markets", "0003_market_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="market",
            name="last_update",
        ),
    ]
