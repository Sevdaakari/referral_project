# Generated by Django 3.2.8 on 2024-04-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0003_auto_20240423_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='verification_code',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
