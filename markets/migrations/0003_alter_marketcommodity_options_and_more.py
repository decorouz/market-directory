# Generated by Django 4.1.1 on 2022-12-11 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("markets", "0002_rename_marketinstance_marketcommodity_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="marketcommodity",
            options={"verbose_name": "market commodities"},
        ),
        migrations.AlterModelTable(
            name="marketcommodity",
            table="sql_market_commodity",
        ),
    ]
