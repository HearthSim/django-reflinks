# Generated by Django 4.0.4 on 2022-05-12 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_reflinks', '0002_referralhit_http_referer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referrallink',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
