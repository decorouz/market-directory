# Generated by Django 4.1.1 on 2022-10-10 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mktdirectory", "0002_commodity_local_name_alter_commodity_grade"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="marketday",
            name="unique_item",
        ),
    ]
