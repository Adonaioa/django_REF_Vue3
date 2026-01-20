# Generated migration for adding admin level field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='level',
            field=models.CharField(
                choices=[
                    ('超级管理员', '超级管理员'),
                    ('管理员', '管理员'),
                    ('管理用户', '管理用户'),
                    ('用户', '用户'),
                ],
                default='用户',
                max_length=20,
                verbose_name='管理员级别'
            ),
        ),
    ]
