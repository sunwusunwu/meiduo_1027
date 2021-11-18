# Generated by Django 3.2.3 on 2021-11-18 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='areas.area', verbose_name='上级行政区')),
            ],
            options={
                'verbose_name': '行政划区',
                'verbose_name_plural': '行政划区',
                'db_table': 'tb_areas',
            },
        ),
    ]
