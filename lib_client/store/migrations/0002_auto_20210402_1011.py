# Generated by Django 3.1.7 on 2021-04-02 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='publishing_hose_name',
            new_name='publishing_house_name',
        ),
    ]
