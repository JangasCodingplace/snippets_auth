# Generated by Django 3.0.6 on 2020-05-14 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_auto_20200514_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='browser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Browser'),
        ),
        migrations.AlterField(
            model_name='client',
            name='deactivating_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Device'),
        ),
        migrations.AlterField(
            model_name='client',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='client',
            name='os',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.OS'),
        ),
        migrations.AlterField(
            model_name='client',
            name='ua_string',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
