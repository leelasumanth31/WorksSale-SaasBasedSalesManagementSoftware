# Generated by Django 3.1.7 on 2021-03-24 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0004_auto_20210324_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownerslists',
            name='expiry_date',
            field=models.DateTimeField(default="2000-05-31 00:00"),
            preserve_default=False,
        ),
    ]
