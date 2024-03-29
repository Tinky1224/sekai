# Generated by Django 4.0.4 on 2022-05-23 12:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Easy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Difficulty', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)])),
            ],
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Difficulty', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)])),
            ],
        ),
        migrations.CreateModel(
            name='Hard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Difficulty', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)])),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Difficulty', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)])),
            ],
        ),
        migrations.CreateModel(
            name='Normal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Difficulty', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)])),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=36)),
                ('num', models.IntegerField(default=999, help_text='Unique ID for its url')),
                ('easy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.easy')),
                ('expert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.expert')),
                ('hard', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.hard')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.master')),
                ('normal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.normal')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('favorite_musics', models.ManyToManyField(blank=True, to='catalog.music')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
