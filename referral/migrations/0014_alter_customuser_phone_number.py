# Generated by Django 3.2.8 on 2024-04-24 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0013_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
