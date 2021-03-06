# Generated by Django 2.2 on 2019-04-13 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_auto_20190409_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='casefile',
            name='is_urgent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='casefile',
            name='last_date_of_hearing',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casefile',
            name='notes',
            field=models.CharField(default='N.A.', max_length=2000),
        ),
        migrations.AddField(
            model_name='casefile',
            name='order',
            field=models.FileField(null=True, upload_to='files/order/'),
        ),
        migrations.AddField(
            model_name='casefile',
            name='order_char',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casefile',
            name='order_pass_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casefile',
            name='order_status',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('REVIEW', 'REVIEW'), ('FINAL', 'FINAL')], default='DRAFT', max_length=15),
        ),
        migrations.AddField(
            model_name='casefile',
            name='party',
            field=models.CharField(default='N.A.', max_length=30),
        ),
        migrations.AddField(
            model_name='casefile',
            name='peshi_char',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casefile',
            name='status',
            field=models.CharField(default='Restricted', max_length=20),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Steno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('permissions', models.ForeignKey(default='LR', on_delete=django.db.models.deletion.CASCADE, to='app.Permission')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Restorer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('permissions', models.ForeignKey(default='LR', on_delete=django.db.models.deletion.CASCADE, to='app.Permission')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='judge',
            name='restorer',
            field=models.ManyToManyField(to='app.Restorer'),
        ),
        migrations.AddField(
            model_name='judge',
            name='steno',
            field=models.ManyToManyField(to='app.Steno'),
        ),
    ]
