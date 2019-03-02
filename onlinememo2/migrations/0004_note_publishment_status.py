# Generated by Django 2.0.5 on 2019-03-02 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinememo2', '0003_note_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='publishment_status',
            field=models.CharField(choices=[('PV', 'Private'), ('PL', 'Public'), ('UR', 'URL')], default='PV', max_length=2),
        ),
    ]