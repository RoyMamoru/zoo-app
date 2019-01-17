# Generated by Django 2.0.10 on 2019-01-17 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('animal_id', models.IntegerField(default=0)),
                ('animal_name', models.CharField(default='', max_length=50)),
                ('animal_title', models.CharField(default='', max_length=300)),
                ('animal_disc', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='ZooCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('animal_id', models.IntegerField(default=0)),
            ],
        ),
    ]