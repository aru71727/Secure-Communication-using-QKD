# Generated by Django 3.0.8 on 2020-07-04 09:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='secret_keys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_key', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='secret_keys_receiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_key', models.CharField(max_length=1000)),
                ('s_index', models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.secret_keys')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=30)),
                ('mobile', models.CharField(max_length=13)),
                ('gender', models.CharField(max_length=6)),
                ('joined_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=30)),
                ('receiver', models.CharField(max_length=30)),
                ('msg_body', models.CharField(max_length=250)),
                ('seen', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('index', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.secret_keys')),
            ],
        ),
    ]
