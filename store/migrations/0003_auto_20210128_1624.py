# Generated by Django 3.1.2 on 2021-01-28 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210128_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('N', 'New'), ('T', 'Trending'), ('X', 'Excel')], max_length=1, null=True),
        ),
    ]
