# Generated by Django 2.1.7 on 2019-04-07 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190405_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casefile',
            name='judges',
        ),
        migrations.AddField(
            model_name='courtroom',
            name='judges',
            field=models.ManyToManyField(to='app.Judge'),
        ),
    ]
