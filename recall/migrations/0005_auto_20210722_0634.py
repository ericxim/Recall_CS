# Generated by Django 3.2.4 on 2021-07-22 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recall', '0004_rename_question_response_questionresponse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionresponse',
            old_name='date_taken',
            new_name='time_taken',
        ),
        migrations.RemoveField(
            model_name='questionresponse',
            name='likes',
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='mark',
            field=models.IntegerField(null=True),
        ),
    ]
