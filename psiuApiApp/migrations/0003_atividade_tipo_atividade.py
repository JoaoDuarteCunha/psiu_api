# Generated by Django 5.1.3 on 2024-11-29 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psiuApiApp', '0002_carona'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='tipo_atividade',
            field=models.TextField(db_column='tipo_atividade', default='Carona'),
            preserve_default=False,
        ),
    ]
