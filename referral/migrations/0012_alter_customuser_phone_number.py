# Generated by Django 3.2.8 on 2024-04-24 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0011_auto_20240424_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]