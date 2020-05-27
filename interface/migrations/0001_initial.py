# Generated by Django 3.0.6 on 2020-05-27 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_sender', models.CharField(max_length=64)),
                ('msg_text', models.CharField(max_length=2048)),
                ('msg_type', models.CharField(max_length=32)),
                ('msg_time', models.DateTimeField(verbose_name='received at time')),
                ('msg_data', models.CharField(max_length=5120)),
            ],
        ),
    ]