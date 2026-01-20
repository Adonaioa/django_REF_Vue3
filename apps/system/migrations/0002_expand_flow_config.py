# Generated migration for expanding FlowConfig model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowconfig',
            name='type',
            field=models.CharField(blank=True, max_length=50, verbose_name='流程类型'),
        ),
        migrations.AddField(
            model_name='flowconfig',
            name='level',
            field=models.CharField(choices=[('普通', '普通审批'), ('重要', '重要审批'), ('紧急', '紧急审批')], default='普通', max_length=20, verbose_name='审批级别'),
        ),
        migrations.AddField(
            model_name='flowconfig',
            name='timeout',
            field=models.IntegerField(default=24, verbose_name='超时时间(小时)'),
        ),
        migrations.AddField(
            model_name='flowconfig',
            name='auto_pass_condition',
            field=models.CharField(blank=True, max_length=200, verbose_name='自动通过条件'),
        ),
        migrations.AddField(
            model_name='flowconfig',
            name='allow_revoke',
            field=models.BooleanField(default=True, verbose_name='是否允许撤回'),
        ),
        migrations.AddField(
            model_name='flowconfig',
            name='allow_transfer',
            field=models.BooleanField(default=False, verbose_name='是否允许转审'),
        ),
        migrations.AddField(
            model_name='flowconfig',
            name='creator',
            field=models.CharField(blank=True, max_length=100, verbose_name='创建人'),
        ),
    ]
