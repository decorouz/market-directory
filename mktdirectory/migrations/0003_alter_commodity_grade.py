# Generated by Django 4.1.1 on 2022-10-03 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mktdirectory", "0002_alter_commodity_grade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commodity",
            name="grade",
            field=models.CharField(
                choices=[("New", "New"), ("Old", "Old"), ("", "")],
                default="",
                max_length=3,
            ),
        ),
    ]
