# Generated by Django 3.1.1 on 2020-10-13 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20201013_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='SorentinoRatio',
            new_name='SortinoRatio',
        ),
        migrations.AddField(
            model_name='stock',
            name='alpha',
            field=models.DecimalField(decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='beta',
            field=models.DecimalField(decimal_places=8, max_digits=10, null=True),
        ),
    ]
