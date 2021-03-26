# Generated by Django 3.1.7 on 2021-03-26 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wharehouse', '0002_book_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='sold',
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold', models.BooleanField(default=False, verbose_name='sold')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wharehouse.book')),
            ],
        ),
    ]