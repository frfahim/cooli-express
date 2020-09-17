# Generated by Django 3.0.8 on 2020-09-13 20:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PickupCoverageDistrict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique Identifier', unique=True, verbose_name='UUID')),
                ('is_available', models.BooleanField(default=True, help_text='if False the record is not available')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PickupCoverageZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique Identifier', unique=True, verbose_name='UUID')),
                ('is_available', models.BooleanField(default=True, help_text='if False the record is not available')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='orders.PickupCoverageDistrict')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
