# Generated by Django 3.1.7 on 2021-03-24 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='date',
        ),
    ]