# Generated by Django 4.0 on 2022-05-31 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_productcategory_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активна'),
        ),
    ]