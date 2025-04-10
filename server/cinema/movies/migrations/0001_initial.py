# Generated by Django 4.2.18 on 2025-03-27 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.SlugField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('longDescription', models.TextField()),
                ('image', models.CharField(max_length=500)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('actor', models.JSONField()),
                ('duration', models.CharField(max_length=500)),
                ('highlight', models.CharField(max_length=500)),
                ('size', models.CharField(max_length=300)),
                ('language', models.CharField(max_length=300)),
                ('releaseDate', models.DateField(blank=True, null=True)),
                ('director', models.CharField(max_length=1000)),
                ('trailerUrl', models.CharField(max_length=1000)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Released', 'Released'), ('Coming Soon', 'Coming Soon'), ('Cancelled', 'Cancelled'), ('Now Showing', 'Now Showing')], default='Pending', max_length=15)),
            ],
        ),
    ]
