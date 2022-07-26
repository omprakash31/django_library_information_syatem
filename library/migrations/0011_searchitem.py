# Generated by Django 4.0.6 on 2022-07-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_book_transaction_cover_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='searchitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('user_id', models.IntegerField(null=True)),
                ('category', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
