# Generated by Django 3.1.7 on 2021-03-26 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0020_auto_20210325_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='todolists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentense', models.CharField(max_length=100)),
            ],
        ),
    ]
