# Generated by Django 5.0.6 on 2025-02-25 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_chat_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pro_pic',
            field=models.FileField(blank=True, null=True, upload_to='profile_pic'),
        ),
    ]
