# Generated by Django 5.0 on 2024-02-24 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_remove_quiz_quiz_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='total_marks',
            new_name='marks_pr_que',
        ),
    ]