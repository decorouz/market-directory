# Generated by Django 4.1.1 on 2022-10-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mktdirectory", "0003_alter_commodity_grade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commodity",
            name="grade",
            field=models.CharField(
                blank=True,
                choices=[("New", "New"), ("Old", "Old"), ("", "")],
                default="New",
                max_length=3,
                null=True,
            ),
        ),
    ]
