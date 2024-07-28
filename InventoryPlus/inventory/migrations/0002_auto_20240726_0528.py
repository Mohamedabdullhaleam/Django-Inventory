# Generated by Django 3.2.25 on 2024-07-26 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='supplier',
        ),
        migrations.AddField(
            model_name='product',
            name='suppliers',
            field=models.ManyToManyField(related_name='products', to='inventory.Supplier'),
        ),
        migrations.AddField(
            model_name='stock',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
