# Generated by Django 5.1 on 2024-08-28 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_rename_address_id_user_address_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="postel_code",
            new_name="postal_code",
        ),
    ]
