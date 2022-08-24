# Generated by Django 4.0.6 on 2022-08-12 01:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_reserved_book_reserve_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_transaction',
            name='deadline',
            field=models.DateField(default=datetime.date(2022, 8, 12), null=True),
        ),
        migrations.AlterField(
            model_name='book_transaction',
            name='issue_date',
            field=models.DateField(default=datetime.date(2022, 8, 12), null=True),
        ),
        migrations.AlterField(
            model_name='invoice_history',
            name='pay_date',
            field=models.DateField(default=datetime.date(2022, 8, 12), null=True),
        ),
        migrations.AlterField(
            model_name='reserved_book',
            name='reserve_date',
            field=models.DateField(default=datetime.date(2022, 8, 12)),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_activity_date',
            field=models.DateField(default=datetime.date(2022, 8, 12), null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='register_date',
            field=models.DateField(default=datetime.date(2022, 8, 12), null=True),
        ),
    ]
