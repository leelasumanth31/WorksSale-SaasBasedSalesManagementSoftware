# Generated by Django 3.1.7 on 2021-03-21 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0002_ownerslists'),
    ]

    operations = [
        migrations.CreateModel(
            name='planlists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('users', models.IntegerField()),
                ('customers', models.IntegerField()),
                ('vendors', models.IntegerField()),
            ],
        ),
    ]
