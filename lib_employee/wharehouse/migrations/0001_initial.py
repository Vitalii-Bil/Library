# Generated by Django 3.1.7 on 2021-03-11 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('bio', models.TextField(blank=True, verbose_name='bio')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date of birth')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=100, verbose_name='title')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('phone', models.CharField(max_length=100, verbose_name='phone number')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price')),
                ('confirmed', models.BooleanField(default=False, verbose_name='confirmed')),
            ],
        ),
        migrations.CreateModel(
            name='PublishingHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('info', models.TextField(blank=True, verbose_name='info')),
                ('year', models.IntegerField(verbose_name='year')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('year', models.IntegerField(verbose_name='year')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='price')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wharehouse.author')),
                ('genre', models.ManyToManyField(to='wharehouse.Genre', verbose_name='genre')),
                ('publishing_house', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wharehouse.publishinghouse')),
            ],
        ),
    ]