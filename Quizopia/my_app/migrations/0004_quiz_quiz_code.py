# Generated by Django 5.0 on 2024-02-24 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_rename_total_marks_quiz_marks_pr_que'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='quiz_code',
            field=models.CharField(default='861188', max_length=50),
        ),
    ]