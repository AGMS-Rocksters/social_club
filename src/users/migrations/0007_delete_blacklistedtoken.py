# Generated by Django 5.1 on 2024-09-04 16:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_merge_0005_alter_user_managers_0005_blacklistedtoken"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BlacklistedToken",
        ),
    ]
