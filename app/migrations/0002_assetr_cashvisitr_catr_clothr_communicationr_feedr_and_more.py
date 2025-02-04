# Generated by Django 4.2.13 on 2024-05-13 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetR',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.asset')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل العهد الثابتة',
            },
            bases=('app.asset',),
        ),
        migrations.CreateModel(
            name='CashVisitR',
            fields=[
                ('cashvisit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.cashvisit')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل مزاورات نقدية',
            },
            bases=('app.cashvisit',),
        ),
        migrations.CreateModel(
            name='CatR',
            fields=[
                ('cat_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.cat')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل القات',
            },
            bases=('app.cat',),
        ),
        migrations.CreateModel(
            name='ClothR',
            fields=[
                ('cloth_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.cloth')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل الملبوسات',
            },
            bases=('app.cloth',),
        ),
        migrations.CreateModel(
            name='CommunicationR',
            fields=[
                ('communication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.communication')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل الإتصالات',
            },
            bases=('app.communication',),
        ),
        migrations.CreateModel(
            name='FeedR',
            fields=[
                ('feed_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.feed')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل التغذية',
            },
            bases=('app.feed',),
        ),
        migrations.CreateModel(
            name='MedicineOrderR',
            fields=[
                ('medicineorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.medicineorder')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': 'دواء',
                'verbose_name_plural': 'تفاصيل الأدوية',
            },
            bases=('app.medicineorder',),
        ),
        migrations.CreateModel(
            name='TransportR',
            fields=[
                ('transport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.transport')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل النقل والتنقلات',
            },
            bases=('app.transport',),
        ),
        migrations.CreateModel(
            name='WaterR',
            fields=[
                ('water_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.water')),
                ('date_gte', models.DateField(verbose_name='من تاريخ')),
                ('date_lte', models.DateField(verbose_name='حتى تاريخ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'تفاصيل الماء',
            },
            bases=('app.water',),
        ),
    ]
