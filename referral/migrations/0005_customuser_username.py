# Generated by Django 3.2.8 on 2024-04-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0004_customuser_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=15),
            preserve_default=False,
        ),
    ]