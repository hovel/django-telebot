# Generated by Django 2.2.2 on 2020-07-16 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemLogRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_class', models.CharField(db_index=True, max_length=50)),
                ('event', models.CharField(max_length=200)),
                ('link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.UserLink')),
            ],
        ),
        migrations.CreateModel(
            name='MessageLogRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.SmallIntegerField(default=0)),
                ('date', models.DateTimeField(db_index=True)),
                ('message', models.TextField(default='')),
                ('success', models.BooleanField(default=True)),
                ('error', models.CharField(max_length=500, null=True)),
                ('message_id', models.IntegerField(null=True)),
                ('addional_info', models.CharField(max_length=500, null=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.UserLink')),
            ],
        ),
    ]