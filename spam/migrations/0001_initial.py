# Generated by Django 4.2.7 on 2024-04-06 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', editable=False, max_length=100)),
                ('phone_no', models.IntegerField()),
                ('email', models.CharField(max_length=50, null=True)),
                ('spam', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('phone_no', models.IntegerField(unique=True)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, null=True)),
                ('spam', models.BooleanField(default=False)),
            ],
        ),
    ]
